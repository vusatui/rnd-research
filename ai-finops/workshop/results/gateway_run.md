# Gateway run (2026-10-19, LiteLLM v1.106.0 self-hosted, shadow prices = frontier card)

Console output of `run_teams.py --setup`, `--traffic --support-max 10 --growth 2`, `--report`:

```
team support  id=fd7338a8-1d25-4d7d-894a-6b8ddd7ce665 budget=$0.05 models=['large', 'small']
team growth   id=9bc4ecb2-bc1b-4f1a-b646-c0daf1b292f3 budget=$0.01 models=['small']
support team -> 'large' until the $0.05 budget trips:
  #01 T01 HTTP 200 in=4222 out=106 team_spend=$0.0
  #02 T02 HTTP 200 in=4209 out=80 team_spend=$0.009504
  #03 T03 HTTP 200 in=4224 out=90 team_spend=$0.018722
  #04 T04 HTTP 200 in=4219 out=122 team_spend=$0.02807
  #05 T05 HTTP 200 in=4221 out=74 team_spend=$0.037728
  #06 T06 HTTP 200 in=4213 out=85 team_spend=$0.04690999999999999
  #07 T07 HTTP 422 in=None out=None team_spend=$0.04690999999999999 Budget has been exceeded! Team=fd7338a8-... Current cost: 0.05618600000000001, Max budget: 0.05
growth team -> tries 'large' (not on its allow-list), then 'small':
  large: HTTP 403 The requested model 'large' is not available for this API key, or the model name is invalid. ...
  small #1 T06 HTTP 200
  small #2 T07 HTTP 200
Team budgets (from the gateway):
  support  spend=$0.05619 / max_budget=$0.05 (112%)
  growth   spend=$0.00091 / max_budget=$0.01 (9%)

Spend logs by team x model (log rows; failed/blocked rows have 0 tokens and $0):
| team | model | requests | prompt tok | completion tok | shadow $ |
|---|---|---|---|---|---|
| growth | large | 1 | 0 | 0 | $0.00000 |
| growth | small | 2 | 8,429 | 144 | $0.00091 |
| support | large | 7 | 25,308 | 557 | $0.05619 |
```

Observations
- The budget is checked **before** a request using spend already recorded, so the request that crosses the line
  is still served: the support team ended at 112% of its budget (one ~$0.0093 request of overshoot). Cloudflare
  documents the same "eventually consistent" behaviour for its spend limits. Size budgets with one request of headroom.
- `team_spend` lags by one request (spend is written asynchronously; `proxy_batch_write_at: 5`).
- The model allow-list is a cost control in itself: the growth team cannot call the expensive model at all (403).
- Gotchas found while building this (LiteLLM OSS v1.106.0):
  1. Key-level `tags` on `/key/generate` returned HTTP 403 "only available for LiteLLM Enterprise users"; per-request
     tags in `metadata.tags` worked and show up in spend logs (`request_tags`).
  2. With the `openrouter/` provider prefix, free-model calls were logged at **$0 even with custom per-token
     prices** (warning: "Billable request priced at $0 ... pricing_not_applied"), so budgets never tripped. Routing
     the same models through the generic OpenAI-compatible provider (`openai/<model>` + `api_base`) applied our
     prices. Root cause (traced later in the v1.106.0 source and reproduced in a 2-call test, see
     `../PARTICIPANTS.md` Exercise 4): `llms/openrouter/chat/transformation.py` copies OpenRouter's own `usage.cost`
     (0 for `:free`) into the `x-litellm-response-cost` hidden header, and `cost_calculator.response_cost_calculator()`
     returns that provider-stated cost before custom prices are considered. Lesson: verify the gateway's cost numbers against a hand calculation
     before trusting budgets built on them.
