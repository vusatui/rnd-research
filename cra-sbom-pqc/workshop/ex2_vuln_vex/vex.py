"""Lab 2b: VEX. Find candidate "not affected" statements with a deliberately simple static check, write an OpenVEX document,
re-scan with grype --vex and measure how many findings disappear.

    python ex2_vuln_vex/vex.py

HONESTY NOTE: a VEX statement is a *claim by the manufacturer*. This script only proposes candidates (direct dependencies that
no first-party file imports); a human must review them before anything is published. It says nothing about transitive
dependencies of used packages, dynamic imports, plugins, or code executed through configuration.
"""
import ast
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import OUT, RESULTS, SAMPLE  # noqa: E402
from ex2_vuln_vex.scan import run_grype  # noqa: E402

# PyPI distribution name -> top-level import name (only where it differs)
IMPORT_NAME = {"pyyaml": "yaml", "pillow": "PIL"}
RELATED = {}   # reserved for hand-written exceptions


def py_direct_deps() -> list[tuple[str, str]]:
    out = []
    for line in (SAMPLE / "py" / "requirements.txt").read_text().splitlines():
        m = re.match(r"^([A-Za-z0-9_.-]+)==([^\s#]+)", line)
        if m:
            out.append((m.group(1).lower(), m.group(2)))
    return out


def npm_direct_deps() -> list[tuple[str, str]]:
    pj = json.loads((SAMPLE / "web" / "package.json").read_text())
    return [(n, v) for n, v in pj["dependencies"].items()]


def py_imports() -> set[str]:
    mods = set()
    for f in (SAMPLE / "py").rglob("*.py"):
        for node in ast.walk(ast.parse(f.read_text())):
            if isinstance(node, ast.Import):
                mods.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                mods.add(node.module.split(".")[0])
    return mods


def js_requires() -> set[str]:
    mods = set()
    for f in (SAMPLE / "web").glob("*.js"):
        mods.update(re.findall(r"require\(['\"]([^'\"./][^'\"]*)['\"]\)", f.read_text()))
        mods.update(re.findall(r"from ['\"]([^'\"./][^'\"]*)['\"]", f.read_text()))
    return mods


def candidates() -> list[dict]:
    used_py, used_js = py_imports(), js_requires()
    c = []
    for name, ver in py_direct_deps():
        if IMPORT_NAME.get(name, name) not in used_py:
            c.append({"purl": f"pkg:pypi/{name}@{ver}", "name": name, "version": ver, "eco": "python"})
    for name, ver in npm_direct_deps():
        if name not in used_js:
            c.append({"purl": f"pkg:npm/{name}@{ver}", "name": name, "version": ver, "eco": "npm"})
    return c


def openvex(cands: list[dict], g: dict) -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    stmts = []
    by_pkg = {}
    for m in g["matches"]:
        by_pkg.setdefault((m["artifact"]["name"].lower(), m["artifact"]["version"]), set()).add(m["vulnerability"]["id"])
    for c in cands:
        for vid in sorted(by_pkg.get((c["name"], c["version"]), [])):
            stmts.append({
                "vulnerability": {"name": vid},
                "products": [{"@id": c["purl"], "identifiers": {"purl": c["purl"]}}],
                "status": "not_affected",
                "justification": "vulnerable_code_not_in_execute_path",
                "impact_statement": (f"{c['name']} is a declared direct dependency, but no first-party source file imports it "
                                     f"(static import check, {ts[:10]}). CANDIDATE: needs human review before publication."),
            })
    return {"@context": "https://openvex.dev/ns/v0.2.0", "@id": "https://example.invalid/vex/acme-gateway/1",
            "author": "Acme Gateway product security (fictional)", "timestamp": ts, "version": 1, "statements": stmts}


def main():
    sbom = OUT / "sbom.enriched.cdx.json"
    before = run_grype(sbom)
    cands = candidates()
    doc = openvex(cands, before)
    vex_path = OUT / "acme-gateway.openvex.json"
    vex_path.write_text(json.dumps(doc, indent=2))
    after = run_grype(sbom, vex_path)
    kev_before = sum(1 for m in before["matches"] if m["vulnerability"].get("knownExploited"))
    kev_after = sum(1 for m in after["matches"] if m["vulnerability"].get("knownExploited"))
    res = {"date": datetime.now().strftime("%Y-%m-%d"), "candidates": [c["purl"] for c in cands],
           "vex_statements": len(doc["statements"]), "grype_matches_before": len(before["matches"]),
           "grype_matches_after_vex": len(after["matches"]), "kev_matches_before": kev_before, "kev_matches_after_vex": kev_after,
           "still_affected_packages": sorted({f'{m["artifact"]["name"]}@{m["artifact"]["version"]}' for m in after["matches"]})}
    (RESULTS / f"ex2_vex_{res['date']}.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
