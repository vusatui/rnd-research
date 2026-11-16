"""Draft the three Art. 14(2) submissions for an actively exploited vulnerability, from a finding in the scan results.

    python ex3_reporting/draft.py [--aware 2026-11-16T09:00:00Z] [--now ...] [--llm]

Deterministic by default. The content follows the *legal* minimum of Art. 14(2)(a)-(c); the ENISA Single Reporting Platform
has its own form fields (see its glossary) - map your draft onto them; we did NOT verify the SRP field list here.
--llm adds ONE free-model call that turns the facts into a plain-language customer advisory (Art. 14(8) "inform the impacted
users"). The model only rephrases facts we give it; a human must read it before it goes out. Free models only.
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import OUT, RESULTS  # noqa: E402
from ex3_reporting.cra_clock import Case, utc  # noqa: E402


def load_finding() -> dict:
    scans = sorted(RESULTS.glob("ex2_scan_*.json"))
    if not scans:
        raise SystemExit("run ex2_vuln_vex/scan.py first")
    kev = json.loads(scans[-1].read_text())["known_exploited"]
    if not kev:
        raise SystemExit("no known-exploited finding in the scan: nothing to report")
    return kev[0]


def early_warning(f: dict, aware: datetime, member_states: list[str]) -> dict:
    """Art. 14(2)(a): early warning, <= 24 h. Minimal on purpose: say what you know, do not wait for completeness."""
    return {"type": "early_warning_actively_exploited_vulnerability", "legal_basis": "Regulation (EU) 2024/2847 Art. 14(2)(a)",
            "manufacturer_aware_at_utc": aware.isoformat(), "vulnerability_ids": [f["cve"], f["advisory"]],
            "affected_product": "Acme Gateway (fictional) - component " + f["package"],
            "member_states_where_product_is_available": member_states,
            "exploitation_evidence": f"listed in CISA KEV since {f['kev_date_added']} ({f['kev_product']}); our own exposure assessment: PENDING",
            "details_still_unknown": ["whether our deployments have been attacked", "affected firmware versions", "workaround"]}


def vulnerability_notification(f: dict, aware: datetime) -> dict:
    """Art. 14(2)(b): <= 72 h, 'unless the relevant information has already been provided'."""
    return {"type": "vulnerability_notification", "legal_basis": "Art. 14(2)(b)",
            "product_general_information": "Acme Gateway device gateway, Python service using Pillow for thumbnails",
            "general_nature_of_exploit_and_vulnerability": f"{f['cve']} ({f['kev_product']}): malformed WebP image parsing; present in the bundled library {f['package']}",
            "corrective_or_mitigating_measures_taken": ["block WebP uploads at the edge (mitigation)", f"upgrade to {', '.join(f['fix'] or [])} or later (corrective, in progress)"],
            "measures_users_can_take": ["disable WebP upload in the console", "install the security update when released"],
            "information_sensitivity": "TLP:AMBER (our assessment; CSIRT may delay dissemination for justified cybersecurity grounds, Art. 16(2))"}


def final_report(f: dict, corrective_at: datetime) -> dict:
    """Art. 14(2)(c): <= 14 days after a corrective OR mitigating measure is available."""
    return {"type": "final_report", "legal_basis": "Art. 14(2)(c)", "corrective_measure_available_utc": corrective_at.isoformat(),
            "description_incl_severity_and_impact": f"{f['cve']}: out-of-bounds write (CWE-787, as listed in the KEV entry) in libwebp, reachable via image upload",
            "malicious_actor_information": "none known to us (where available)",
            "security_update_details": f"Pillow >= {', '.join(f['fix'] or [])} shipped in firmware 2.4.1 (fictional)"}


def user_advisory_llm(facts: dict) -> str:
    from common.llm import chat
    prompt = ("Write a 90-word customer security advisory in plain English for operators of a device gateway. "
              "Use ONLY these facts, add nothing, no marketing, no promises:\n" + json.dumps(facts, indent=1))
    return chat([{"role": "system", "content": "You write short, factual security advisories."},
                 {"role": "user", "content": prompt}], max_tokens=300, temperature=0.2).strip()


UNSUPPORTED = ["critical", "remote code execution", "rce", "arbitrary code", "data breach", "no evidence", "ransomware",
               "guarantee", "fully protected", "immediately"]


def advisory_guard(text: str, facts: dict) -> list[str]:
    """Cheap fact guard: risk words the model used that are NOT in the facts we gave it (severity inflation is the usual failure)."""
    low, base = text.lower(), json.dumps(facts).lower()
    return [w for w in UNSUPPORTED if w in low and w not in base]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aware", default="2026-11-16T09:00:00Z"); ap.add_argument("--now", default=None)
    ap.add_argument("--llm", action="store_true")
    a = ap.parse_args()
    aware = utc(a.aware); now = utc(a.now) if a.now else aware + timedelta(hours=20)
    f = load_finding()
    case = Case("vulnerability", aware)
    case.sent["early_warning"] = aware + timedelta(hours=19, minutes=30)
    case.corrective_measure_at = aware + timedelta(days=2, hours=6)   # mitigation (WebP block) live
    out = {"finding": f, "clock": case.status(now),
           "early_warning": early_warning(f, aware, ["DE", "NL"]),
           "vulnerability_notification": vulnerability_notification(f, aware),
           "final_report": final_report(f, case.corrective_measure_at)}
    if a.llm:
        from common.llm import MODEL
        facts = {"cve": f["cve"], "component": f["package"], "fix": f["fix"], "mitigation": "block WebP uploads", "exploited": True}
        out["user_advisory_llm"] = user_advisory_llm(facts)
        out["user_advisory_model"] = MODEL
        out["user_advisory_unsupported_claims"] = advisory_guard(out["user_advisory_llm"], facts)
    (OUT / "cra_drafts.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
