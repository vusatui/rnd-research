"""Lab 1: generate an SBOM with syft, measure it against CRA / BSI / CISA yardsticks, enrich it, measure again.

    python ex1_sbom/run_sbom.py            # writes out/sbom.cdx.json, out/sbom.enriched.cdx.json, results/ex1_sbom_*.json
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # run from anywhere

import time
from datetime import date

from common.paths import OUT, RESULTS, SAMPLE, tool
from ex1_sbom.check_sbom import check, render, summary_pct
from ex1_sbom.enrich import enrich


def main():
    syft = tool("syft")
    raw, enriched = OUT / "sbom.cdx.json", OUT / "sbom.enriched.cdx.json"
    t0 = time.time()
    subprocess.run([syft, f"dir:{SAMPLE}", "-q", "-o", f"cyclonedx-json={raw}", "-o", f"spdx-json={OUT / 'sbom.spdx.json'}"],
                   check=True)
    dt = time.time() - t0
    ver = subprocess.run([syft, "--version"], capture_output=True, text=True).stdout.strip()
    bom = json.loads(raw.read_text())
    before = check(bom)
    print(f"{ver}: {len(bom['components'])} components in {dt:.1f} s, CycloneDX {bom['specVersion']}\n")
    print("=== BEFORE (raw syft output) ===")
    print(render(before))
    stats = enrich(bom, json.loads((SAMPLE / "web" / "package-lock.json").read_text()),
                   "security@acme-gateway.example", "Acme Gateway product security (fictional)")
    enriched.write_text(json.dumps(bom, indent=2))
    after = check(bom)
    print(f"=== AFTER enrich.py ({stats}) ===")
    print(render(after))
    res = {"date": str(date.today()), "tool": ver, "seconds": round(dt, 2), "components": before["components"],
           "spec_version": bom["specVersion"], "enrich_stats": stats,
           "before": before["checks"], "after": after["checks"],
           "summary_pct_before": summary_pct(before), "summary_pct_after": summary_pct(after)}
    (RESULTS / f"ex1_sbom_{date.today()}.json").write_text(json.dumps(res, indent=2))
    print("summary % before:", res["summary_pct_before"])
    print("summary % after: ", res["summary_pct_after"])


if __name__ == "__main__":
    main()
