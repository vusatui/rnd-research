"""Runs the original CBACT04C (interest calculation batch job) under GnuCOBOL.

This is the left side of the "diamond": the running legacy program is the
source of truth. We emulate the INTCALC JCL: DD names become DD_* environment
variables, PARM='2022071800' is passed through the RUNPARM driver, VSAM KSDS
files are GnuCOBOL indexed files loaded from the CardDemo ASCII extracts.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import tempfile
from dataclasses import dataclass

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / "build"
DATA = HERE.parent / "vendor" / "carddemo" / "app" / "data" / "ASCII"


@dataclass
class LegacyResult:
    return_code: int         # process exit status (Linux keeps only the low 8 bits: 999 -> 231!)
    abend_code: int | None   # user abend code reported by the CEE3ABD shim, e.g. 999
    stdout: str
    stderr: str
    transactions: list[str]  # 350-byte TRAN-RECORDs written to TRANSACT
    accounts: list[str]      # 300-byte ACCOUNT-RECORDs after the job


def _ensure_built():
    if not (BUILD / "CBACT04C.so").exists():
        subprocess.run([str(HERE / "build.sh")], check=True)


def run_intcalc(accounts: list[str], xrefs: list[str], discgrps: list[str], tcatbals: list[str],
                parm: str = "2022071800") -> LegacyResult:
    _ensure_built()
    with tempfile.TemporaryDirectory(prefix="intcalc-") as tmp:
        t = pathlib.Path(tmp)
        env = {**os.environ, "COB_LIBRARY_PATH": str(BUILD), "COB_SET_TRACE": "N"}
        dd = {"ACCTFILE": t / "acct.ksds", "XREFFILE": t / "xref.ksds", "DISCGRP": t / "disc.ksds",
              "TCATBALF": t / "tcat.ksds", "TRANSACT": t / "systran.dat", "OUTFILE": t / "acct.out"}
        env.update({f"DD_{k}": str(v) for k, v in dd.items()})
        # KSDS load requires ascending keys, exactly like IDCAMS REPRO into a KSDS.
        for kind, rows, keylen in (("ACCT", accounts, 11), ("XREF", xrefs, 16),
                                   ("DISC", discgrps, 16), ("TCAT", tcatbals, 17)):
            src = t / f"{kind}.txt"
            src.write_text("\n".join(sorted(rows, key=lambda r: r[:keylen])) + "\n", encoding="latin-1")
            subprocess.run([str(BUILD / "loadksds"), kind], env={**env, "DD_INFILE": str(src)},
                           check=True, capture_output=True, text=True)
        proc = subprocess.run([str(BUILD / "runparm"), "CBACT04C", parm], env=env,
                              capture_output=True, text=True, encoding="latin-1")
        subprocess.run([str(BUILD / "dumpacct")], env=env, check=True, capture_output=True)
        raw = dd["TRANSACT"].read_bytes().decode("latin-1") if dd["TRANSACT"].exists() else ""
        trans = [raw[i:i + 350] for i in range(0, len(raw), 350)] if raw else []
        accts = [ln.ljust(300) for ln in dd["OUTFILE"].read_text(encoding="latin-1").splitlines()]
        m = re.search(r"CEE3ABD USER ABEND ([+-]?\d+)", proc.stderr)
        abend = int(m.group(1)) if m else None
        return LegacyResult(proc.returncode, abend, proc.stdout, proc.stderr, trans, accts)


def carddemo_inputs():
    from common.records import ACCOUNT_LEN, DISCGRP_LEN, TCATBAL_LEN, XREF_LEN, read_fixed
    return dict(accounts=read_fixed(DATA / "acctdata.txt", ACCOUNT_LEN),
                xrefs=read_fixed(DATA / "cardxref.txt", XREF_LEN),
                discgrps=read_fixed(DATA / "discgrp.txt", DISCGRP_LEN),
                tcatbals=read_fixed(DATA / "tcatbal.txt", TCATBAL_LEN))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE.parent))
    r = run_intcalc(**carddemo_inputs())
    print("RC", r.return_code, "| transactions:", len(r.transactions), "| accounts:", len(r.accounts))
    print(r.stdout[-600:], r.stderr[-400:])
