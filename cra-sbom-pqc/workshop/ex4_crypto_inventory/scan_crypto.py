"""Lab 4: crypto inventory (CBOM) + quantum-risk ranking for a source tree.

    python ex4_crypto_inventory/scan_crypto.py [path]          # default: sample_app
    python ex4_crypto_inventory/scan_crypto.py --z 8,12,15     # sensitivity of the ranking to the CRQC-arrival assumption

Outputs: out/cbom.cdx.json (CycloneDX 1.6 cryptographic-asset components) and a ranked migration backlog.
The ranking uses Mosca's inequality  X + Y > Z  (X = how long the data/signature must stay secure, Y = how long migration takes,
Z = years until a CRQC exists). Z is NOBODY'S fact: it is a parameter you must set and defend; we print the result for several Z.
"""
import argparse
import json
import re
import sys
import uuid
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import OUT, RESULTS, SAMPLE  # noqa: E402
from ex4_crypto_inventory.rules import KEY_BITS, RULES, SKIP_DIRS, SUFFIXES  # noqa: E402

ASSETS = Path(__file__).with_name("assets.json")


def scan(root: Path) -> list[dict]:
    findings = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or set(f.parts) & SKIP_DIRS or f.suffix not in SUFFIXES or f.name in ("package-lock.json", "requirements.txt"):
            continue
        try:
            lines = f.read_text().splitlines()
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(lines, 1):
            if line.lstrip().startswith(("#", "//", "*", "/*")) and "ssl_" not in line:   # skip comments (config keys excepted)
                continue
            for rule in RULES:
                if rule.pattern.search(line):
                    bits = None
                    for k in KEY_BITS:   # key size on the same or next two lines
                        m = next((k.search(l) for l in lines[i - 1:i + 2] if k.search(l)), None)
                        if m:
                            bits = int(m.group(1)); break
                    findings.append({"family": rule.family, "primitive": rule.primitive, "function": rule.function,
                                     "quantum": rule.quantum, "pqc_target": rule.pqc_target, "curve": rule.curve,
                                     "file": str(f.relative_to(root)), "line": i, "code": line.strip()[:110],
                                     "key_bits": bits if rule.family == "RSA" else None})
    return findings


def match_asset(f: dict, assets: list[dict]) -> dict | None:
    for a in assets:
        if a["file"] == f["file"] and a["family"] == f["family"] and re.search(a.get("code_regex", "."), f["code"]):
            return a
    return None


def rank(findings: list[dict], assets: list[dict], zs: list[int]) -> list[dict]:
    """One row per business asset (several rules can fire on the same asset); sorted by X+Y, longest first."""
    groups: dict[str, dict] = {}
    for f in findings:
        if f["quantum"] != "broken-by-Shor":
            continue
        a = match_asset(f, assets)
        name = a["asset"] if a else f"UNMAPPED ({f['file']}) - ask the owner"
        g = groups.setdefault(name, {"asset": name, "purpose": a["purpose"] if a else "?", "x": a["x_years_secure"] if a else None,
                                     "y": a["y_years_to_migrate"] if a else None, "families": set(), "locations": set()})
        g["families"].add(f["family"]); g["locations"].add(f"{f['file']}:{f['line']}")
    rows = []
    for g in groups.values():
        x, y = g["x"], g["y"]
        g["families"], g["locations"] = sorted(g["families"]), sorted(g["locations"])
        g["verdict"] = {str(z): (("MIGRATE NOW" if x + y > z else "plan") if x is not None else "?") for z in zs}
        rows.append(g)
    return sorted(rows, key=lambda r: -((r["x"] + r["y"]) if r["x"] is not None else 99))


def cbom(findings: list[dict], root: Path) -> dict:
    comps = {}
    for f in findings:
        key = (f["family"], f.get("key_bits"), f.get("curve"))
        c = comps.setdefault(key, {
            "type": "cryptographic-asset", "bom-ref": f"crypto/{len(comps)}/{f['family'].replace(' ', '-')}", "name": f["family"],
            "cryptoProperties": {"assetType": "algorithm", "algorithmProperties": {
                "primitive": f["primitive"], "cryptoFunctions": [],
                "nistQuantumSecurityLevel": 0 if f["quantum"] in ("broken-by-Shor", "classically-broken") else 1}},
            "evidence": {"occurrences": []}, "properties": [
                {"name": "workshop:quantum", "value": f["quantum"]}, {"name": "workshop:pqc-target", "value": f["pqc_target"]}]})
        if f.get("key_bits"):
            c["cryptoProperties"]["algorithmProperties"]["parameterSetIdentifier"] = str(f["key_bits"])
        if f.get("curve"):
            c["cryptoProperties"]["algorithmProperties"]["curve"] = f["curve"]
        c["evidence"]["occurrences"].append({"location": f["file"], "line": f["line"]})
    return {"$schema": "http://cyclonedx.org/schema/bom-1.6.schema.json", "bomFormat": "CycloneDX", "specVersion": "1.6",
            "serialNumber": f"urn:uuid:{uuid.uuid4()}", "version": 1,
            "metadata": {"timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "tools": {"components": [{"type": "application", "name": "workshop scan_crypto.py", "version": "1"}]},
                         "component": {"type": "application", "name": root.name}},
            "components": list(comps.values())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=str(SAMPLE)); ap.add_argument("--z", default="8,12,15")
    a = ap.parse_args()
    root = Path(a.path); zs = [int(z) for z in a.z.split(",")]
    findings = scan(root)
    assets = json.loads(ASSETS.read_text())["assets"] if root == SAMPLE else []
    ranked = rank(findings, assets, zs)
    bom = cbom(findings, root)
    (OUT / "cbom.cdx.json").write_text(json.dumps(bom, indent=2))
    by_family = defaultdict(int)
    for f in findings:
        by_family[(f["family"], f["quantum"])] += 1
    print(f"{len(findings)} findings in {len({f['file'] for f in findings})} files; CBOM components: {len(bom['components'])}\n")
    for (fam, q), n in sorted(by_family.items(), key=lambda kv: kv[0][1]):
        print(f"  {fam:<28} {q:<20} {n:>3}")
    print(f"\nQuantum-vulnerable, ranked by X+Y (years); verdict for Z = {zs}:")
    for r in ranked:
        v = " ".join(f"Z={z}:{r['verdict'][str(z)]:<11}" for z in zs)
        print(f"  X={r['x']!s:<4} Y={r['y']!s:<3} {v} {r['asset']}  [{', '.join(r['families'])}; {len(r['locations'])} loc]")
    res = {"date": str(date.today()), "findings": len(findings), "files": len({f['file'] for f in findings}),
           "by_family": {f"{k[0]} [{k[1]}]": n for k, n in by_family.items()}, "z_assumptions_years": zs,
           "ranked": ranked, "findings_detail": findings}
    (RESULTS / f"ex4_inventory_{date.today()}.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
