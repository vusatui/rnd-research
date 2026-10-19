"""Per-team attribution and budget enforcement through a self-hosted LiteLLM gateway.

    ./up.sh                         # LiteLLM + Postgres on 127.0.0.1:4000
    python run_teams.py --setup     # create teams + virtual keys (admin, master key)
    python run_teams.py --traffic   # send tickets as two teams until the support budget trips
    python run_teams.py --report    # spend by team / key / model / tag from the gateway's own logs

Teams (shadow dollars, frontier price card, see litellm_config.yaml):
  support: max_budget $0.05, models [large, small]
  growth:  max_budget $0.01, models [small] only (model allow-list = a cost policy)
Note: key-level `tags` are a LiteLLM Enterprise feature (HTTP 403 on OSS v1.106.0), so attribution here uses
teams + keys + key metadata; per-request tags are sent in request metadata.
Free-quota cost of --traffic: ~10-14 requests.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.pipeline import CONFIGS, build_messages, load_tickets  # noqa: E402
from common.paths import OUT  # noqa: E402

BASE = os.environ.get("LITELLM_BASE", "http://127.0.0.1:4000")
MASTER = os.environ.get("LITELLM_MASTER_KEY", "sk-workshop-master-change-me")
STATE = OUT / "gateway_keys.json"   # git-ignored: contains virtual keys


def api(method: str, path: str, body: dict | None = None, key: str = MASTER):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, {"raw": raw}


def setup():
    teams = {"support": {"max_budget": 0.05, "models": ["large", "small"]},
             "growth": {"max_budget": 0.01, "models": ["small"]}}
    state = {}
    for alias, t in teams.items():
        code, team = api("POST", "/team/new", {"team_alias": alias, "max_budget": t["max_budget"],
                                               "budget_duration": "30d", "models": t["models"],
                                               "metadata": {"cost_center": f"cc-{alias}"}})
        assert code == 200, (code, team)
        code, key = api("POST", "/key/generate", {"team_id": team["team_id"], "key_alias": f"{alias}-bot",
                                                  "models": t["models"],
                                                  "metadata": {"app": f"{alias}-bot"}})
        assert code == 200, (code, key)
        state[alias] = {"team_id": team["team_id"], "key": key["key"], "max_budget": t["max_budget"]}
        print(f"team {alias:8} id={team['team_id']} budget=${t['max_budget']} models={t['models']}")
    STATE.write_text(json.dumps(state, indent=1))


def chat(key: str, model: str, messages: list[dict], tags: list[str]):
    body = {"model": model, "messages": messages, "max_tokens": 350, "temperature": 0,
            "reasoning": {"enabled": False}, "metadata": {"tags": tags}}
    t0 = time.time()
    code, r = api("POST", "/chat/completions", body, key)
    return code, r, time.time() - t0


def traffic(n_support: int, n_growth: int):
    state = json.loads(STATE.read_text())
    tickets = load_tickets()
    log = []
    cfg = CONFIGS["C_stable"]   # full knowledge base, stable prefix, concise
    print("support team -> 'large' until the $0.05 budget trips:")
    for i in range(n_support):
        t = tickets[i % len(tickets)]
        code, r, dt = chat(state["support"]["key"], "large", build_messages(t, cfg), ["ticket-reply", t["id"]])
        msg = (r.get("error") or {}).get("message", "")[:150] if code != 200 else ""
        u = r.get("usage", {}) if code == 200 else {}
        _, info = api("GET", f"/team/info?team_id={state['support']['team_id']}")
        spend = (info.get("team_info") or {}).get("spend")
        print(f"  #{i+1:02} {t['id']} HTTP {code} in={u.get('prompt_tokens')} out={u.get('completion_tokens')} "
              f"team_spend=${spend if spend is not None else '?'} {msg}")
        log.append({"team": "support", "i": i + 1, "ticket": t["id"], "code": code, "team_spend": spend, "error": msg})
        if code != 200 and "budget" in msg.lower():
            break
        time.sleep(6)   # let the proxy flush spend to Postgres (proxy_batch_write_at: 5)
    print("growth team -> tries 'large' (not on its allow-list), then 'small':")
    code, r, _ = chat(state["growth"]["key"], "large", build_messages(tickets[0], cfg), ["ticket-reply"])
    msg = (r.get("error") or {}).get("message", "")[:160]
    print(f"  large: HTTP {code} {msg}")
    log.append({"team": "growth", "model": "large", "code": code, "error": msg})
    for i in range(n_growth):
        t = tickets[(i + 5) % len(tickets)]
        code, r, dt = chat(state["growth"]["key"], "small", build_messages(t, CONFIGS["F_small_full"]),
                           ["ticket-reply", t["id"]])
        msg = (r.get("error") or {}).get("message", "")[:150] if code != 200 else ""
        print(f"  small #{i+1} {t['id']} HTTP {code} {msg}")
        log.append({"team": "growth", "model": "small", "ticket": t["id"], "code": code, "error": msg})
        time.sleep(6)
    (OUT / "gateway_traffic.json").write_text(json.dumps(log, indent=1))


def report():
    state = json.loads(STATE.read_text())
    time.sleep(6)
    print("Team budgets (from the gateway):")
    for alias, s in state.items():
        _, info = api("GET", f"/team/info?team_id={s['team_id']}")
        ti = info.get("team_info", {})
        print(f"  {alias:8} spend=${ti.get('spend', 0):.5f} / max_budget=${ti.get('max_budget')} "
              f"({(ti.get('spend', 0) or 0) / ti.get('max_budget', 1):.0%})")
    code, logs = api("GET", "/spend/logs?summarize=false")
    if code != 200 or not isinstance(logs, list):
        print("spend logs unavailable:", code, str(logs)[:200])
        return
    team_names = {s["team_id"]: a for a, s in state.items()}
    agg: dict[tuple, dict] = {}
    for row in logs:
        key = (team_names.get(row.get("team_id"), row.get("team_id")), row.get("model_group") or row.get("model"))
        a = agg.setdefault(key, {"requests": 0, "spend": 0.0, "prompt_tokens": 0, "completion_tokens": 0})
        a["requests"] += 1
        a["spend"] += row.get("spend") or 0
        a["prompt_tokens"] += row.get("prompt_tokens") or 0
        a["completion_tokens"] += row.get("completion_tokens") or 0
    print("\nSpend logs by team x model (successful requests are billed; blocked ones are not):")
    print("| team | model | requests | prompt tok | completion tok | shadow $ |\n|---|---|---|---|---|---|")
    for (team, model), a in sorted(agg.items(), key=lambda x: str(x[0])):
        print(f"| {team} | {model} | {a['requests']} | {a['prompt_tokens']:,} | {a['completion_tokens']:,} | "
              f"${a['spend']:.5f} |")
    (OUT / "gateway_spend_logs.json").write_text(json.dumps(logs, indent=1, default=str))
    print(f"\nraw spend logs: {OUT / 'gateway_spend_logs.json'} (input for to_focus.py)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--setup", action="store_true")
    ap.add_argument("--traffic", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--support-max", type=int, default=10)
    ap.add_argument("--growth", type=int, default=2)
    a = ap.parse_args()
    if a.setup:
        setup()
    if a.traffic:
        traffic(a.support_max, a.growth)
    if a.report:
        report()
    if not (a.setup or a.traffic or a.report):
        ap.print_help()
