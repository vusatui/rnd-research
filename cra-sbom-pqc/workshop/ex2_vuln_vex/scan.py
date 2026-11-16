"""Lab 2a: scan the SBOM (grype) and the lockfiles (osv-scanner), compare, and flag known-exploited findings.

    python ex2_vuln_vex/scan.py [--no-kev-fetch]

Why two scanners: they use different databases and matching rules; the overlap is the interesting number.
Why KEV: Art. 14 CRA is triggered by an *actively exploited* vulnerability ("reliable evidence that a malicious actor
has exploited it", Art. 3(42)). CISA's KEV catalogue is one public source of such evidence - NOT the legal test.
"""
import json
import subprocess
import sys
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import OUT, RESULTS, SAMPLE, tool  # noqa: E402

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def run_grype(sbom: Path, vex: Path | None = None) -> dict:
    cmd = [tool("grype"), f"sbom:{sbom}", "-o", "json", "-q"]
    if vex:
        cmd += ["--vex", str(vex)]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)


def run_osv() -> dict:
    out = OUT / "osv.json"
    subprocess.run([tool("osv-scanner"), "scan", "source", "--lockfile", str(SAMPLE / "web" / "package-lock.json"),
                    "--lockfile", str(SAMPLE / "py" / "requirements.txt"), "--format", "json",
                    "--output-file", str(out)], capture_output=True, text=True)   # exit 1 = vulns found
    return json.loads(out.read_text())


def grype_set(g: dict) -> set[tuple[str, str]]:
    return {(m["artifact"]["name"].lower(), m["artifact"]["version"]) for m in g["matches"]}


def osv_set(o: dict) -> set[tuple[str, str]]:
    return {(p["package"]["name"].lower(), p["package"]["version"])
            for r in o["results"] for p in r["packages"] if p.get("vulnerabilities")}


def grype_ids(g: dict) -> set[str]:
    ids = set()
    for m in g["matches"]:
        ids.add(m["vulnerability"]["id"])
        ids.update(r["id"] for r in m.get("relatedVulnerabilities", []))
    return ids


def osv_ids(o: dict) -> set[str]:
    ids = set()
    for r in o["results"]:
        for p in r["packages"]:
            for v in p.get("vulnerabilities", []):
                ids.add(v["id"]); ids.update(v.get("aliases", []))
    return ids


def kev_hits(g: dict, fetch: bool) -> list[dict]:
    """Known-exploited findings: grype's embedded KEV data, cross-checked against the live CISA catalogue."""
    live = None
    if fetch:
        try:
            live = {v["cveID"] for v in json.load(urllib.request.urlopen(KEV_URL, timeout=30))["vulnerabilities"]}
        except Exception as e:  # offline is fine
            print("(live KEV fetch failed:", e, ")")
    hits = {}
    for m in g["matches"]:
        for k in m["vulnerability"].get("knownExploited") or []:
            hits[(m["artifact"]["name"], m["artifact"]["version"], m["vulnerability"]["id"], k["cve"])] = {
                "package": f'{m["artifact"]["name"]}@{m["artifact"]["version"]}', "advisory": m["vulnerability"]["id"],
                "cve": k["cve"], "kev_date_added": k["dateAdded"], "kev_product": f'{k["vendorProject"]} {k["product"]}',
                "fix": m["vulnerability"].get("fix", {}).get("versions"),
                "in_live_kev": (k["cve"] in live) if live is not None else None}
    return list(hits.values())


def main():
    fetch = "--no-kev-fetch" not in sys.argv
    sbom = OUT / "sbom.enriched.cdx.json"
    if not sbom.exists():
        raise SystemExit("run ex1_sbom/run_sbom.py first")
    g, o = run_grype(sbom), run_osv()
    gs, os_ = grype_set(g), osv_set(o)
    gi, oi = grype_ids(g), osv_ids(o)
    sev = {}
    for m in g["matches"]:
        sev[m["vulnerability"]["severity"]] = sev.get(m["vulnerability"]["severity"], 0) + 1
    with_fix = sum(1 for m in g["matches"] if m["vulnerability"].get("fix", {}).get("versions"))
    kev = kev_hits(g, fetch)
    res = {
        "date": str(date.today()),
        "grype_db_built": g["descriptor"]["db"]["status"]["built"],
        "grype": {"matches": len(g["matches"]), "vulnerable_packages": len(gs), "by_severity": sev, "with_fix": with_fix,
                  "distinct_ids_incl_aliases": len(gi)},
        "osv_scanner": {"vulnerable_packages": len(os_), "distinct_ids_incl_aliases": len(oi),
                        "vulns": sum(len(p.get("vulnerabilities", [])) for r in o["results"] for p in r["packages"])},
        "package_overlap": {"both": len(gs & os_), "grype_only": sorted(gs - os_), "osv_only": sorted(os_ - gs)},
        "id_overlap": {"both": len(gi & oi), "grype_only": len(gi - oi), "osv_only": len(oi - gi)},
        "known_exploited": kev,
    }
    (RESULTS / f"ex2_scan_{date.today()}.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
