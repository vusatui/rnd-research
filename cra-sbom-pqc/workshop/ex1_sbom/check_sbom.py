"""Machine-checkable subset of SBOM requirements, applied to a CycloneDX JSON file.

Three yardsticks, all read from the primary documents (see ../../research.md):
  * CRA Annex I Part II(1): machine-readable, commonly used format, at least top-level dependencies  (law)
  * BSI TR-03183-2 v2.1.0: required fields (a German technical guideline; it is NOT a presumption of conformity)
  * CISA et al. "2026 Minimum Elements for an SBOM" (July 2026; US-led, voluntary guidance)
Only what can be decided from the JSON alone is checked; semantic quality (is the licence right? is the list complete?)
cannot. Each check returns (passed, total) so the result is a coverage ratio.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def _contact(obj: dict) -> bool:
    """BSI: an e-mail address, or if none exists a URL, of the creator. A bare name is not enough."""
    for key in ("authors", "manufacturer", "supplier", "author"):
        v = obj.get(key)
        items = v if isinstance(v, list) else [v] if v else []
        for it in items:
            if not isinstance(it, dict):
                continue
            if it.get("email") or it.get("url"):
                return True
            for c in it.get("contact") or []:
                if c.get("email"):
                    return True
    return False


def _producer(c: dict) -> bool:
    return bool(c.get("supplier") or c.get("manufacturer") or c.get("author") or c.get("authors"))


def _sha512(c: dict) -> bool:
    return any(h.get("alg") == "SHA-512" for h in c.get("hashes") or [])


def _any_hash(c: dict) -> bool:
    return bool(c.get("hashes"))


def _license(c: dict) -> bool:
    return bool(c.get("licenses"))


def _ident(c: dict) -> bool:
    return bool(c.get("purl") or c.get("cpe") or c.get("swid"))


def _ext(c: dict, *types: str) -> bool:
    return any(r.get("type") in types and r.get("url") for r in c.get("externalReferences") or [])


def check(bom: dict) -> dict:
    comps = [c for c in bom.get("components", []) if c.get("type") != "file"]
    n = len(comps)
    meta = bom.get("metadata", {})
    tools = meta.get("tools", {})
    tool_list = tools.get("components", []) if isinstance(tools, dict) else tools
    depref = {d["ref"] for d in bom.get("dependencies", []) if d.get("dependsOn") is not None}
    refs_with_dep = sum(1 for c in comps if c.get("bom-ref") in depref)

    def frac(pred) -> tuple[int, int]:
        return sum(1 for c in comps if pred(c)), n

    one = lambda ok: (1 if ok else 0, 1)  # noqa: E731
    r = {
        "CRA Annex I Part II(1)": {
            "machine-readable common format (CycloneDX/SPDX JSON)": one(bom.get("bomFormat") == "CycloneDX"),
            "top-level dependencies listed (components present)": one(n > 0),
        },
        "BSI TR-03183-2 v2.1.0 (SBOM-level)": {
            "creator with e-mail or URL": one(_contact(meta)),
            "timestamp": one(bool(meta.get("timestamp"))),
            "SBOM URI (serialNumber)": one(bool(bom.get("serialNumber"))),
            "CycloneDX >= 1.6": one(tuple(int(x) for x in str(bom.get("specVersion", "0.0")).split(".")) >= (1, 6)),
        },
        "BSI TR-03183-2 v2.1.0 (per component)": {
            "component creator with e-mail or URL": frac(_contact),
            "name": frac(lambda c: bool(c.get("name"))),
            "version": frac(lambda c: bool(c.get("version"))),
            "dependency relationships present": (refs_with_dep, n),
            "licence": frac(_license),
            "SHA-512 hash of the deployable": frac(_sha512),
            "unique identifier (purl/CPE/SWID)": frac(_ident),
            "source-code URI": frac(lambda c: _ext(c, "source-distribution", "vcs")),
            "URI of the deployable form": frac(lambda c: _ext(c, "distribution")),
        },
        "CISA 2026 Minimum Elements (SBOM-level)": {
            "SBOM Author": one(bool(meta.get("authors") or meta.get("manufacturer") or meta.get("supplier"))),
            "SBOM Author Signature": one(bool(bom.get("signature"))),
            "Data Format Name + Version": one(bool(bom.get("bomFormat") and bom.get("specVersion"))),
            "Generation Context (lifecycles)": one(bool(meta.get("lifecycles"))),
            "SBOM Tool Name + Version": one(any(t.get("name") and t.get("version") for t in tool_list)),
            "SBOM Version": one("version" in bom),
            "SBOM Timestamp": one(bool(meta.get("timestamp"))),
            "Coverage declared (compositions)": one(bool(bom.get("compositions"))),
        },
        "CISA 2026 Minimum Elements (per component)": {
            "Component Producer": frac(_producer),
            "Component Hash (value + algorithm)": frac(_any_hash),
            "Component License": frac(_license),
            "Component Identifiers": frac(_ident),
        },
    }
    return {"components": n, "checks": r}


def render(res: dict) -> str:
    out = [f"components checked: {res['components']}", ""]
    for group, items in res["checks"].items():
        out.append(f"{group}")
        for name, (ok, tot) in items.items():
            pct = 100 * ok / tot if tot else 0
            out.append(f"  {name:<55} {ok:>3}/{tot:<3} {pct:5.1f}%")
        out.append("")
    return "\n".join(out)


def summary_pct(res: dict) -> dict:
    s = {}
    for g, items in res["checks"].items():
        ok = sum(a for a, _ in items.values())
        tot = sum(b for _, b in items.values())
        s[g] = round(100 * ok / tot, 1) if tot else 0.0
    return s


if __name__ == "__main__":
    bom = json.loads(Path(sys.argv[1]).read_text())
    print(render(check(bom)))
