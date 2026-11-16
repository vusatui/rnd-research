"""CRA Art. 14 reporting clock: deadlines from the moment the manufacturer "becomes aware".

Source: Regulation (EU) 2024/2847, Art. 14(2) (actively exploited vulnerability) and 14(4) (severe incident); applies from 11 Sep 2026
(Art. 71(2)). Deadlines are wall-clock (24 h, 72 h, 14 days, one month) - the text has no business-day exclusion.
"Without undue delay and in any event within ..." means the stated time is the *outer* bound, not a target.

What this code does NOT decide: whether something is an "actively exploited vulnerability" (Art. 3(42): reliable evidence of
exploitation without the system owner's permission), whether an incident is "severe" (Art. 14(5)), or when you "became aware"
(a legal and factual question - document it). The tool only does the arithmetic and the bookkeeping.
"""
from __future__ import annotations

import calendar
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

KINDS = ("vulnerability", "incident")


def add_months(dt: datetime, months: int) -> datetime:
    """Calendar month arithmetic (31 Jan + 1 month = 28/29 Feb): 'within one month after ...'. A legal reading may differ; see research.md."""
    m = dt.month - 1 + months
    y, m = dt.year + m // 12, m % 12 + 1
    return dt.replace(year=y, month=m, day=min(dt.day, calendar.monthrange(y, m)[1]))


@dataclass
class Case:
    kind: str                                   # "vulnerability" | "incident"
    aware_at: datetime
    corrective_measure_at: datetime | None = None   # vulnerability: when a corrective OR MITIGATING measure is available
    notification_72h_sent_at: datetime | None = None  # incident: final report is due one month after THIS submission
    sent: dict = field(default_factory=dict)    # {"early_warning": dt, "notification": dt, "final_report": dt}

    def __post_init__(self):
        assert self.kind in KINDS
        for f in ("aware_at", "corrective_measure_at", "notification_72h_sent_at"):
            v = getattr(self, f)
            if v is not None and v.tzinfo is None:
                raise ValueError(f"{f} must be timezone-aware (use UTC)")

    def deadlines(self) -> dict[str, datetime | None]:
        d = {"early_warning": self.aware_at + timedelta(hours=24),
             "notification": self.aware_at + timedelta(hours=72)}
        if self.kind == "vulnerability":
            d["final_report"] = (self.corrective_measure_at + timedelta(days=14)) if self.corrective_measure_at else None
        else:
            base = self.sent.get("notification") or self.notification_72h_sent_at
            d["final_report"] = add_months(base, 1) if base else None
        return d

    def status(self, now: datetime) -> list[dict]:
        rows = []
        for name, due in self.deadlines().items():
            sent = self.sent.get(name)
            if due is None:
                state, left = "NOT STARTED (clock starts when " + (
                    "a corrective or mitigating measure is available" if self.kind == "vulnerability"
                    else "the 72 h incident notification is submitted") + ")", None
            elif sent:
                state, left = ("SENT ON TIME" if sent <= due else "SENT LATE"), None
            else:
                left = due - now
                state = "OVERDUE" if left.total_seconds() < 0 else "open"
            rows.append({"step": name, "due_utc": due.isoformat() if due else None, "state": state,
                         "time_left": _fmt(left) if left is not None else None})
        return rows


def _fmt(td: timedelta) -> str:
    s = int(td.total_seconds()); sign = "-" if s < 0 else ""; s = abs(s)
    return f"{sign}{s // 86400}d {s % 86400 // 3600:02d}h {s % 3600 // 60:02d}m"


def utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser(description="CRA Art. 14 clock. Example: python ex3_reporting/cra_clock.py vulnerability --aware 2026-11-16T09:00:00Z --now 2026-11-17T10:00:00Z")
    ap.add_argument("kind", choices=KINDS); ap.add_argument("--aware", required=True)
    ap.add_argument("--corrective"); ap.add_argument("--notified-72h"); ap.add_argument("--now")
    ap.add_argument("--sent-early-warning"); ap.add_argument("--sent-notification")
    a = ap.parse_args()
    c = Case(a.kind, utc(a.aware), utc(a.corrective) if a.corrective else None, utc(a.notified_72h) if a.notified_72h else None)
    if a.sent_early_warning: c.sent["early_warning"] = utc(a.sent_early_warning)
    if a.sent_notification: c.sent["notification"] = utc(a.sent_notification)
    now = utc(a.now) if a.now else datetime.now(timezone.utc)
    print(f"now: {now.isoformat()}")
    for r in c.status(now):
        print(f"  {r['step']:<14} due {r['due_utc'] or '-':<27} {r['state']:<12} {r['time_left'] or ''}")
