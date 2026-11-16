"""Honest SBOM enrichment: add only what we can *derive or know*, never invent.

Derived from the lockfile: SHA-512 (npm `integrity`) and the `resolved` URL of each npm package.
Known to us (config): who authors this SBOM (--author-email), the lifecycle phase, and that the Python part is only
the direct pins (requirements.txt has no transitive closure) -> declared as `incomplete` via `compositions`.
What we do NOT invent: component creators/suppliers, licences, source URIs. Those stay missing - that is the point of the gap report.
"""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path


def npm_integrity(lock: dict) -> dict[tuple[str, str], tuple[str, str]]:
    out = {}
    for path, pkg in lock.get("packages", {}).items():
        if not path or "integrity" not in pkg:
            continue
        name = path.split("node_modules/")[-1]
        algo, b64 = pkg["integrity"].split("-", 1)
        out[(name, pkg["version"])] = (algo, base64.b64decode(b64).hex(), pkg.get("resolved", ""))
    return out


def enrich(bom: dict, lock: dict, author_email: str, author_name: str) -> dict:
    integ = npm_integrity(lock)
    added_hash = added_uri = 0
    for c in bom.get("components", []):
        hit = integ.get((c.get("name"), c.get("version")))
        if hit and hit[0] == "sha512":
            c.setdefault("hashes", []).append({"alg": "SHA-512", "content": hit[1]})
            added_hash += 1
            if hit[2]:
                c.setdefault("externalReferences", []).append({"type": "distribution", "url": hit[2]})
                added_uri += 1
    meta = bom.setdefault("metadata", {})
    meta["authors"] = [{"name": author_name, "email": author_email}]
    meta["lifecycles"] = [{"phase": "build"}]
    py = [c["bom-ref"] for c in bom["components"] if c.get("purl", "").startswith("pkg:pypi/")]
    npm = [c["bom-ref"] for c in bom["components"] if c.get("purl", "").startswith("pkg:npm/")]
    bom["compositions"] = [
        {"aggregate": "incomplete", "assemblies": py},   # requirements.txt lists direct pins only
        {"aggregate": "complete", "assemblies": npm},    # package-lock.json lists the full tree
    ]
    return {"hashes_added": added_hash, "uris_added": added_uri}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sbom"); ap.add_argument("lockfile"); ap.add_argument("out")
    ap.add_argument("--author-email", default="security@acme-gateway.example")
    ap.add_argument("--author-name", default="Acme Gateway product security (fictional)")
    a = ap.parse_args()
    bom = json.loads(Path(a.sbom).read_text())
    stats = enrich(bom, json.loads(Path(a.lockfile).read_text()), a.author_email, a.author_name)
    Path(a.out).write_text(json.dumps(bom, indent=2))
    print(stats)
