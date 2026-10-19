# Participant guide: make an LLM feature's bill visible, attributable and smaller

You will take a small support-reply feature for a fictional SaaS, **Ledgerly** (a 10-section knowledge base, 16
customer tickets with deterministic checks), and measure what each cost lever really does to **$ per successful
task** *and* to quality. Then you put a self-hosted gateway with per-team budgets in front of it, produce a
FOCUS-shaped chargeback file, and work out when self-hosting a model pays off.

Everything is free: free OpenRouter models and open-source LiteLLM + Postgres in Docker.
Time: ~2.5 h. Facilitator agenda and full measured results: [`../workshop-plan.md`](../workshop-plan.md).

> The outputs below come from the measured runs on 2026-10-19 committed in [`results/`](results/) and from a
> clean-clone verification run the same day (Linux, Python 3.13, LiteLLM v1.106.0). Models: large =
> `nvidia/nemotron-3-ultra-550b-a55b:free`, small = `nvidia/nemotron-3.5-lightning:free`. LLM outputs will differ
> on your machine; with n=16 tickets and one run per configuration, a difference of 1-2 tickets is noise.

**Shadow cost.** Free calls cost $0, which hides exactly the problem this workshop is about. Every call is therefore
priced from published list prices, and nothing is ever charged:
- *twin*: the paid OpenRouter endpoint of the same model (fetched live from `/api/v1/models`);
- *frontier*: a paid frontier price card (large = gpt-6.1-sol $2.00 in / $10.00 out per 1M tokens, small =
  gpt-6-luna $0.10 / $0.50; read 2026-10-19 from platform.openai.com/docs/pricing). Edit them in
  [`common/pricing.py`](common/pricing.py).

## 1. Prerequisites

| What | Version | Check |
|---|---|---|
| git | any | `git --version` |
| Python | 3.11+ | `python3 --version` |
| Docker | any recent; only for Exercise 4 (gateway) | `docker run --rm hello-world` |
| Free ports | `4000` (LiteLLM) and `55432` (Postgres) on 127.0.0.1, Exercise 4 only | `ss -ltn \| grep -E ':4000\|:55432'` prints nothing |
| OpenRouter key | free account | needed for Exercises 1, 2a and 4; Exercises 2b, 3 and 5 and all re-scoring are offline |

Pre-pull the gateway images on a good connection (~1.6 GB together):
`docker pull ghcr.io/berriai/litellm:v1.106.0 && docker pull postgres:16-alpine`.

### Get a free OpenRouter key

1. Sign up at <https://openrouter.ai>, open <https://openrouter.ai/keys>, create a key. No credit card is needed for `:free` models.
2. **Use free models only** (ids ending in `:free`). The defaults in [`common/llm.py`](common/llm.py) are free; the
   prices you see in the reports are shadow prices.
3. Never commit the key. It goes into `workshop/.env`, which is git-ignored.

### Know your free quota

From the [OpenRouter limits page](https://openrouter.ai/docs/api-reference/limits) (checked 2026-10-19): free models
allow **20 requests/min**, plus **50 requests/day** if you have bought fewer than 10 credits in total, or **1,000/day**
if you have bought at least 10. The daily counter resets at 00:00 UTC. The client in `common/llm.py` throttles
itself to 18 requests/min.

| Part | LLM requests |
|---|---|
| Ex1: one configuration on all 16 tickets | 16 |
| Ex1: all nine configurations (A-I) | ~146 (cascades add one call per escalation) |
| Ex1: re-scoring committed runs (`--rescore`) | 0 |
| Ex2a: `cache_probe.py --n 4 --pad 1` (both prefixes) | 8 |
| Ex2b: `caching_sim.py` | 0 |
| Ex3: semantic cache | 0 (one-time ~70 MB embedding-model download, or `--lexical`) |
| Ex4: gateway traffic (`--support-max 10 --growth 2`) | ~10 |
| Ex4: the `openrouter/` pitfall demo | 2 |
| Ex5: break-even | 0 |
| **Whole workshop as we ran it** | **~230** |

On the **50/day tier**, run Exercise 1 with `--only T01,T05,T11` (3 requests per configuration) and use the committed
runs for the full picture: `--rescore`, the caching simulator, the semantic cache and the break-even need no LLM.
Check what is left at any time:

```
$ python check_quota.py
free-model requests today (UTC day): used 224 / limit 1000 -> remaining 776
the full workshop as run used ~230 requests; with a 50/day limit use --only (see README.md)
```

## 2. Setup (10 min)

```bash
git clone https://github.com/vusatui/rnd-research.git
cd rnd-research/ai-finops/workshop
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pip install fastembed                # optional: embeddings for Exercise 3 (otherwise use --lexical)
cp .env.example .env                 # then put your key into OPENROUTER_API_KEY=
python -m pytest -q tests            # offline: no network, no key
python list_free_models.py           # current free models and their paid-twin prices
python check_quota.py                # free requests left today
```

Expected (verification run):

```
.......                                                                  [100%]
7 passed in 0.13s

nvidia/nemotron-3-super-120b-a12b:free                  tools ctx=  262144  paid twin $0.08/$0.45 per 1M in/out
nvidia/nemotron-3-ultra-550b-a55b:free                  tools ctx= 1000000  paid twin $0.60/$2.40 per 1M in/out
nvidia/nemotron-3.5-lightning:free                      tools ctx= 1000000  paid twin $0.07/$0.20 per 1M in/out
...
```

The 7 offline tests cover the knowledge base and BM25 retrieval, the cost math, the ticket checks, the cascade's
escalation logic, byte-identical stable prefixes (needed for prompt caching), the number-grounding check, and a smoke
run of the offline scripts.

`.env` options (see [`.env.example`](.env.example)):

| Variable | Meaning |
|---|---|
| `OPENROUTER_API_KEY` | your key (required for live LLM steps) |
| `LARGE_MODEL` / `SMALL_MODEL` | the free model pair. If one vanished, pick a replacement from `list_free_models.py` **that has a paid twin** (no paid twin = no twin shadow price) |
| `OPENROUTER_RPM` | client-side throttle, default 18 requests/min |
| `LITELLM_MASTER_KEY` | admin key of the local gateway (Exercise 4). The default is a workshop placeholder; everything listens on 127.0.0.1 only |

Everything a run produces goes to `out/` (git-ignored): raw runs, the call ledger `out/ledger.jsonl`, CSVs. The
curated results from our runs are in `results/`.

## 3. Exercise 1 - Lever lab: $ per successful task (45 min)

**Goal:** run the same 16 tickets through different configurations and read cost *and* quality side by side.
Predict each result before you run it.

| Config | What changes |
|---|---|
| `A_baseline` | large model, whole knowledge base in the prompt, a dynamic header (timestamp + ticket id) first, verbose answer, `max_tokens` 1500 |
| `B_concise` | + short JSON answer, `max_tokens` 350 |
| `C_stable` | + dynamic header moved into the user turn (stable prefix) |
| `D_trim` | + BM25 top-3 knowledge-base sections instead of the whole knowledge base |
| `E_small_dyn` / `F_small_full` / `G_small_trim` | small model (dynamic prefix / stable prefix / trimmed context) |
| `H_cascade` | small model first; escalate to the large model if the JSON is invalid or self-reported confidence < 0.75 |
| `I_cascade_grounded` | H + escalate if the reply contains a `$` amount, `%` or number that is not in the knowledge base or ticket |

### 1a. Re-score the committed runs first (no LLM, 1 second)

```bash
python ex2_levers/run_levers.py --rescore results/levers_A-H_2026-10-19.json
python ex2_levers/run_levers.py --rescore results/levers_I_2026-10-19.json
```

Expected:

```
| config | pass | avg in tok | cache hit | avg out tok | $/task (twin) | $/task (frontier) | $/success (frontier) | vs base (frontier) | p50 s | calls |
|---|---|---|---|---|---|---|---|---|---|---|
| A_baseline | 14/16 | 4,231 | 0% | 403 | $0.003507 | $0.01250 | $0.01428 | +0% | 8.85 | 16 |
| B_concise | 15/16 | 4,216 | 0% | 85 | $0.002734 | $0.00928 | $0.00990 | -26% | 2.32 | 16 |
| C_stable | 14/16 | 4,218 | 0% | 88 | $0.002741 | $0.00931 | $0.01064 | -25% | 2.77 | 16 |
| D_trim | 15/16 | 1,537 | 0% | 86 | $0.001129 | $0.00394 | $0.00420 | -68% | 3.76 | 16 |
| E_small_dyn | 14/16 | 4,217 | 0% | 79 | $0.000311 | $0.00046 | $0.00053 | -96% | 4.31 | 16 |
| F_small_full | 14/16 | 4,217 | 0% | 79 | $0.000311 | $0.00046 | $0.00053 | -96% | 2.64 | 16 |
| G_small_trim | 9/16 | 1,537 | 0% | 82 | $0.000124 | $0.00019 | $0.00035 | -98% | 1.9 | 16 |
| H_cascade | 13/16 | 4,039 | 3% | 81 | $0.000354 | $0.00065 | $0.00080 | -95% | 1.83 | 17 |

| I_cascade_grounded | 14/16 | 4,310 | 15% | 87 | $0.000362 | $0.00065 | $0.00074 | +0% | 1.52 | 17 |
```

(`vs base` is relative to `A_baseline` within the same file, so the separate I file shows `+0%`; against A it is -95%.)
Per-ticket answers and failures are in the JSON files; [`app/checks.py`](app/checks.py) defines what "pass" means.

### 1b. Run it live

```bash
python ex2_levers/run_levers.py --configs A_baseline,B_concise,D_trim,F_small_full,I_cascade_grounded   # ~82 requests
# low on quota: 3 tickets per config, including the T11 pricing trap
python ex2_levers/run_levers.py --configs B_concise,I_cascade_grounded --only T01,T11 --workers 2         # 4-5 requests
```

Expected for the small run (verification run):

```
B_concise     T01 PASS in= 4220 cached=    0 out= 105 $0.00949
B_concise     T11 PASS in= 4223 cached=    0 out= 144 $0.00989
I_cascade_grounded T01 PASS in= 4222 cached=    0 out= 104 $0.00047
I_cascade_grounded T11 PASS in= 5711 cached=    0 out= 238 $0.00478 esc(ungrounded numbers ['$5940'])
...
LLM calls: 5  saved: .../out/levers_<stamp>.json
```

T11 asks what the Enterprise plan costs. The knowledge base says "custom pricing". In this run the small model
invented "$5,940", the grounding check saw a `$` amount that is not in the knowledge base and escalated to the large
model, which answered correctly. That one escalation cost ~10x a small-model answer and still came in at ~half of
the large model's cost per ticket.

**What to observe:**
- **Output is expensive.** In A, ~400 output tokens at 5x the input price were about a third of the cost. B's short
  JSON answer was -26% cheaper, *better* (15/16), and p50 latency fell from 8.9 s to 2.3 s.
- **Trimming context is the biggest lever on the large model** (-68%) with no quality loss here.
- **Levers interact.** Small model alone: 14/16. Trimming alone: 15/16. Both together (G): 9/16. Re-run the eval set
  after every lever.
- **A cascade is only as good as its escalation signal.** In the committed H run the small model invented an
  Enterprise price with self-reported confidence 0.95, so H did not escalate. Only the deterministic number check (I)
  caught it. A naive version of that check once let "$5,000" through because "5,000" appears in the knowledge base as
  a file count; comparing with the `$` sign fixed it.
- **The checks have blind spots too:** F "passed" T11 once with an invented price because the reply also said
  "contact sales for a custom quote". Quality numbers are only as good as the checks.
- **The price card changes the business case.** Large vs small differs ~9x on twin prices and ~20x on the frontier
  card. Always state which card and which date.

**Stretch:** add a ticket that needs two knowledge-base sections and watch D/G's BM25 recall; add a config that caps
`max_tokens` at 150 and find where answers start to break; price the run with your own price card in
`common/pricing.py`.

## 4. Exercise 2 - Prompt caching (20 min)

**Goal:** see whether the provider actually caches a stable prefix, and what caching would save under published
provider rules.

### 2a. Probe (8 requests, sequential, small model)

```bash
python ex2_levers/cache_probe.py --n 4 --pad 1 --prefixes dynamic,stable     # ~8k-token prompt
```

What we measured (`results/cacheprobe-*.json`): with the ~4.2k-token prompt both prefixes got **0 cached tokens**.
With the ~8.1k-token prompt (`--pad 1`), the stable prefix got **6,288 cached tokens** on every request from the
2nd on (58% of input, twin cost -24%), the dynamic prefix 0. In the script's output format
(from [`results/cacheprobe-20261019-165014.json`](results/cacheprobe-20261019-165014.json)):

```
dynamic  T01 in=8142 cached=0 provider=Nvidia $0.000591
...
stable   T01 in=8141 cached=0 provider=Nvidia $0.000590
stable   T02 in=8129 cached=6288 provider=Nvidia $0.000396
stable   T03 in=8144 cached=6288 provider=Nvidia $0.000395
stable   T04 in=8142 cached=6288 provider=Nvidia $0.000407

dynamic : cache hit rate 0% of input tokens, twin cost $0.002356 for 4 requests
stable  : cache hit rate 58% of input tokens, twin cost $0.001788 for 4 requests
```

Caching on free endpoints is undocumented and opportunistic (a later run cached 15% of ~4.2k prompts), so read the
probe qualitatively.

### 2b. Simulate published rules (offline)

```bash
python ex2_levers/caching_sim.py results/levers_A-H_2026-10-19.json --config C_stable
```

Expected:

```
C_stable: avg input 4,218 tok = stable prefix ~4,173 + per-ticket ~45

Input-token cost multiplier vs no caching, by requests sharing the prefix within one TTL window:
| provider rule | N=1 | N=2 | N=5 | N=20 | N=100 |
|---|---|---|---|---|---|
| no caching | 1.00x | 1.00x | 1.00x | 1.00x | 1.00x |
| OpenAI GPT-5.6+ (0.10x) | 1.25x | 0.68x | 0.34x | 0.17x | 0.12x |
| OpenAI gpt-6.1-sol (0.05x) | 1.25x | 0.65x | 0.30x | 0.12x | 0.07x |
| Anthropic 5-min (0.10x) | 1.25x | 0.68x | 0.34x | 0.17x | 0.12x |
| Anthropic 1-hour (0.10x) | 1.99x | 1.05x | 0.49x | 0.20x | 0.13x |
| Gemini implicit (0.05x) | 1.00x | 0.53x | 0.25x | 0.11x | 0.07x |
```

**What to observe:**
- **One dynamic value at the top of the prompt (time, request id, user name) kills caching.** Every request becomes
  "N=1": with a write premium you pay *more* than without caching and never read the cache.
- Caching needs volume within the TTL. N=2 already roughly halves input cost; a 1-hour cache only pays at N≥3.
- Providers have a minimum cacheable length; our 4.2k prompt got nothing on the free endpoint, the 8k prompt did.

**Stretch:** move the ticket id back into the system prompt of C and re-run the probe; compute the break-even N for
the 1-hour rule by hand.

## 5. Exercise 3 - Semantic cache: when "similar" is wrong (15 min, offline)

**Goal:** a semantic cache returns a stored answer when a new question is "similar enough". Sweep the threshold on
24 hand-built pairs ([`ex3_semantic_cache/pairs.jsonl`](ex3_semantic_cache/pairs.jsonl)): 12 true paraphrases and
12 near-misses that need a *different* answer.

```bash
python ex3_semantic_cache/semantic_cache.py            # bge-small-en-v1.5 via fastembed (first run downloads ~70 MB)
python ex3_semantic_cache/semantic_cache.py --lexical  # no download: character 3-gram TF-IDF
```

Expected with embeddings (identical in the verification run):

```
similarity (bge-small-en-v1.5 embeddings): paraphrases mean 0.824 [min 0.676, max 0.919] | near-misses mean 0.836 [min 0.680, max 0.946]
exact-match cache: 0/12 paraphrase hits, 0/12 false hits

| threshold | paraphrase hits (saved calls) | near-miss hits (WRONG answers served) |
|---|---|---|
| 0.70 | 11/12 | 10/12 |
| 0.75 | 11/12 | 9/12 |
| 0.80 | 8/12 | 9/12 |
| 0.85 | 3/12 | 6/12 |
| 0.90 | 2/12 | 4/12 |
| 0.95 | 0/12 | 0/12 |

Worst near-misses (highest similarity, different answer):
  0.946  'Is SAML SSO available on the Business plan?'  vs  'Is SAML SSO available on the Enterprise plan?'
  0.932  'How do I export all my invoices?'  vs  'How do I import all my invoices?'
```

With `--lexical`: no paraphrase is ever hit, and 2/12 near-misses still are at 0.70-0.85.

**What to observe:**
- Near-misses are on average *more* similar than paraphrases (0.836 vs 0.824). No single threshold separates them.
- A wrong cached answer costs $0 and is served instantly: the saving is visible on the bill, the damage is not.
- The pairs are adversarial by design; real traffic has fewer near-misses. That is an argument for measuring on
  your own traffic, not for trusting a default threshold.

**Stretch:** add entity checks (plan names, "import"/"export") before serving a hit and re-run the sweep; scope the
cache key by plan or tenant.

## 6. Exercise 4 - Gateway: team budgets, allow-lists, chargeback (40 min, Docker)

**Goal:** put a self-hosted LiteLLM gateway in front of the feature, give two teams virtual keys with budgets and
model allow-lists, trip a budget, and turn the gateway's spend logs into a FOCUS-shaped chargeback.

| Team | Budget (shadow $) | Allowed models |
|---|---|---|
| `support` | $0.05 | `large`, `small` |
| `growth` | $0.01 | `small` only |

```bash
./ex4_gateway/up.sh                                    # LiteLLM on 127.0.0.1:4000 (UI at /ui), Postgres on 127.0.0.1:55432
python ex4_gateway/run_teams.py --setup                # teams + virtual keys -> out/gateway_keys.json (git-ignored)
python ex4_gateway/run_teams.py --traffic --support-max 10 --growth 2    # ~10 requests, ~3 min (6 s between calls)
python ex4_gateway/run_teams.py --report               # budgets + spend logs -> out/gateway_spend_logs.json
python ex4_gateway/to_focus.py --gateway               # FOCUS-shaped CSV + chargeback from the gateway's logs
python ex4_gateway/to_focus.py                         # the same from the local ledger (needs a live Ex1/Ex2 run)
```

No Docker or no quota? Use the committed logs: `python ex4_gateway/to_focus.py --gateway results/gateway_spend_logs_reduced.json`.

Expected (verification run; the committed run is in [`results/gateway_run.md`](results/gateway_run.md)):

```
waiting for LiteLLM (first start runs DB migrations, can take a few minutes).......... up: http://127.0.0.1:4000

team support  id=653ac324-... budget=$0.05 models=['large', 'small']
team growth   id=002ae608-... budget=$0.01 models=['small']
support team -> 'large' until the $0.05 budget trips:
  #01 T01 HTTP 200 in=4223 out=105 team_spend=$0.0
  #02 T02 HTTP 200 in=4211 out=80 team_spend=$0.009496000000000001
  #03 T03 HTTP 200 in=4221 out=91 team_spend=$0.018718
  #04 T04 HTTP 200 in=4217 out=122 team_spend=$0.02807
  #05 T05 HTTP 503 in=None out=None team_spend=$0.02807 litellm.ServiceUnavailableError: ... Upstream error from Nvidia: Service temporarily overloaded
  #06 T06 HTTP 200 in=4210 out=85 team_spend=$0.03772399999999999
  #07 T07 HTTP 200 in=4218 out=100 team_spend=$0.04699399999999999
  #08 T08 HTTP 422 in=None out=None team_spend=$0.05642999999999999 Budget has been exceeded! Team=653ac324-... Current cost: 0.05643, Max budget: 0.05
growth team -> tries 'large' (not on its allow-list), then 'small':
  large: HTTP 403 The requested model 'large' is not available for this API key, or the model name is invalid. ...
  small #1 T06 HTTP 200
Team budgets (from the gateway):
  support  spend=$0.05643 / max_budget=$0.05 (113%)
  growth   spend=$0.00045 / max_budget=$0.01 (5%)

16 FOCUS-shaped rows from 8 calls -> .../out/focus_gateway.csv          # committed logs (results/...reduced.json)
| team | config | model | direction | cache | tokens | ListCost $ |
|---|---|---|---|---|---|---|
| growth | gateway:small | nemotron-3.5-lightning | Input | Uncached | 8,429 | 0.000590 |
| growth | gateway:small | nemotron-3.5-lightning | Output | Uncached | 144 | 0.000029 |
| support | gateway:large | nemotron-3-ultra-550b-a55b | Input | Uncached | 25,308 | 0.015185 |
| support | gateway:large | nemotron-3-ultra-550b-a55b | Output | Uncached | 557 | 0.001337 |
```

The 503 was a real upstream overload on the free endpoint (no retries are configured on purpose, see "What to
observe"). The committed run had no 503 and tripped at request 7 with 112%.

**What to observe:**
- **Budgets overshoot by one request.** The check runs *before* a call against spend already recorded, so the call
  that crosses the line is served (112-113%). Team spend shown to the client lags by one request
  (`proxy_batch_write_at: 5`). Size budgets with one request of headroom.
- **The allow-list is a cost control in itself:** `growth` cannot call the expensive model at all (HTTP 403).
- **Chargeback is per principal, not per key secret:** `PrincipalId` is the key *alias*. Key-level `tags` are an
  Enterprise feature in LiteLLM (HTTP 403 on OSS v1.106.0); per-request `metadata.tags` work and land in `request_tags`.
- Failed and blocked calls appear in the spend logs with $0. LiteLLM may still record an estimated prompt-token count
  for them (in our verification run the failed 503 row carried 3,926 prompt tokens), so `--report`'s token totals can be
  higher than `to_focus.py`'s, which keeps only successful calls.
- `to_focus.py` writes FOCUS 1.4 column names plus FOCUS 1.5 *draft* properties (`ModelId`, `TokenDirection`,
  `TokenCacheAction`) in `SkuPriceDetails`; `BilledCost` is 0 (free tier) and `ListCost` is the twin shadow cost. It
  is not validated against the FOCUS validator. Note the gateway budgets use the *frontier* card from
  `litellm_config.yaml`, while `to_focus.py` uses *twin* prices: two cards, two numbers. Say which one a report uses.

### The `$0` pitfall: why the config uses `openai/`, not `openrouter/`

LiteLLM has a native OpenRouter provider (`model: openrouter/<id>`). With it, **free models are logged at $0 even
when you set custom per-token prices, so budgets never trip.** Our first gateway run fell into this. Reproduce it
with the `small-openrouter-prefix` alias in [`ex4_gateway/litellm_config.yaml`](ex4_gateway/litellm_config.yaml)
(same model, same custom prices, not on any team's allow-list, so call it with the master key; 2 requests):

```bash
for m in small small-openrouter-prefix; do
  curl -s -D - -o /dev/null http://127.0.0.1:4000/chat/completions \
    -H "Authorization: Bearer ${LITELLM_MASTER_KEY:-sk-workshop-master-change-me}" -H 'Content-Type: application/json' \
    -d "{\"model\":\"$m\",\"messages\":[{\"role\":\"user\",\"content\":\"Say OK\"}],\"max_tokens\":5,\"reasoning\":{\"enabled\":false}}" \
    | grep -i '^x-litellm-response-cost:\|^llm_provider-x-litellm-response-cost:'
done
docker logs finops-litellm 2>&1 | grep 'priced at \$0' | tail -1
```

Expected (verification run, 18 prompt + 2 completion tokens each):

```
x-litellm-response-cost: 2.8e-06                     # small: 18 x $0.10/1M + 2 x $0.50/1M = $0.0000028
llm_provider-x-litellm-response-cost: 0.0          # small-openrouter-prefix: OpenRouter's own cost wins
LiteLLM:WARNING: ... Billable request priced at $0 and logged as such (model_group=small-openrouter-prefix
  model=openrouter/nvidia/nemotron-3.5-lightning:free provider=openrouter prompt_tokens=18 completion_tokens=2):
  pricing entry '...' declares non-zero rates for this usage, but the cost calculator returned $0.
  Counted in litellm_zero_cost_requests_total{reason="pricing_not_applied"}
```

The spend logs (`/spend/logs`) show the same: `small` $0.0000028, `small-openrouter-prefix` $0.0.

**Root cause** (traced in the LiteLLM v1.106.0 source in the image, not reported upstream):
1. `llms/openrouter/chat/transformation.py` adds `usage: {include: true}` to every request and copies OpenRouter's
   own `usage.cost` from the response into the hidden header `llm_provider-x-litellm-response-cost`.
2. `cost_calculator.response_cost_calculator()` returns that provider-stated cost as soon as it is present, *before*
   it calls `completion_cost()`, which is where custom prices are applied.
3. OpenRouter reports `usage.cost: 0` for `:free` models, so the custom price is never used. A zero-cost request also
   skips budget checks by design (LiteLLM's "zero-cost models" feature), so nothing ever blocks.

**Fix (what the config does):** route OpenRouter through the generic OpenAI-compatible provider and put the custom
prices on the deployment:

```yaml
  - model_name: small
    litellm_params:
      model: openai/nvidia/nemotron-3.5-lightning:free     # generic provider, not openrouter/
      api_base: https://openrouter.ai/api/v1
      api_key: os.environ/OPENROUTER_API_KEY
      input_cost_per_token: 0.0000001                      # $0.10 per 1M (shadow price)
      cache_read_input_token_cost: 0.00000001
      output_cost_per_token: 0.0000005                     # $0.50 per 1M
```

The [LiteLLM custom pricing docs](https://docs.litellm.ai/docs/proxy/custom_pricing) show the same keys under
`model_info`; we verified only the `litellm_params` placement above. Turning usage accounting off is not a way
around it: in our test OpenRouter returned `usage.cost` even on the `openai/` route, where nothing asked for it (the
generic provider simply ignores the field). On paid OpenRouter models the provider-stated cost is the *real* bill,
which is what you want; the pitfall only bites when you need a price other than what OpenRouter charges (free models,
internal chargeback rates, a negotiated discount).

**Lesson:** before trusting a budget, check one request's logged cost against a hand calculation.

```bash
./ex4_gateway/down.sh       # stops and removes both containers; spend data in Postgres is discarded
```

**Stretch:** add a `budget_duration: 1d` key-level budget for one user; add a third team with an `rpm_limit`; send
`metadata.tags: ["feature:billing-faq"]` and build a chargeback by feature; price the gateway with twin prices
instead of the frontier card and compare the team totals.

## 7. Exercise 5 - Self-host break-even (15 min, offline)

**Goal:** when does a self-hosted open model beat an API? Every assumption is a flag.

```bash
python ex5_breakeven/breakeven.py
python ex5_breakeven/breakeven.py --gpu-hour 10      # hyperscaler-like GPU price
python ex5_breakeven/breakeven.py --help             # --gpus --tps --ops-month --in-out --prefill-x ...
```

Expected (default assumptions: 8xH100 at $3.50/GPU-h always on, $15k/month ops, an **assumed** 5,000 output tok/s):

```
Replica: 8 GPUs x $3.5/h = $20,440/month always-on, + ops $15,000 = $35,440/month fixed
Capacity at 100% utilization: 6.57B output tokens/month (+10x input tokens each)

| API | API $ per 1M output tok (incl. its input) | self-host break-even volume | break-even utilization |
|---|---|---|---|
| open-weights via API (0.60/2.40) | $8.40 | 4.22B out tok/month | 64% |
| frontier API (2.00/10.00) | $30.00 | 1.18B out tok/month | 18% |
```

With `--gpu-hour 10` the open-weights row becomes `133% (impossible: >100%)` and the frontier row 37%.

**What to observe:**
- Break-even is a **utilization** question. Business-hours-only traffic (50 of 168 h/week) caps an always-on replica
  at ~30% average utilization.
- The frontier row compares different models: it only matters if your evals show the open model is good enough.
- The throughput is the weakest assumption; measure it for your model and prompt shape before deciding.

**Stretch:** model a replica that scales to zero outside business hours; add the people cost of an on-call rotation.

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `Set OPENROUTER_API_KEY` | `cp .env.example .env` and fill in the key, or `export OPENROUTER_API_KEY=...` |
| HTTP 429 `free-models-per-min` | the 20 requests/min limit is per account, so switching models does not help. The client throttles to 18 rpm; do not run two scripts in parallel, lower `--workers` or `OPENROUTER_RPM` |
| HTTP 429 / 503 from the upstream provider ("temporarily overloaded"), `ERROR` in a ticket row, `no choices` | by design there are **no retries and no fallbacks** (a silent retry is a silent extra charge and hides which model answered). The ticket counts as failed; re-run it with `--only <id>` |
| Daily quota exhausted (HTTP 429 mentioning the daily free-model limit) | 50 or 1,000/day, resets 00:00 UTC. `python check_quota.py`; continue offline with `--rescore results/...`, `caching_sim.py`, the semantic cache, `breakeven.py` and `to_focus.py --gateway results/gateway_spend_logs_reduced.json` |
| A model id no longer exists / "No endpoints found" | free models rotate: `python list_free_models.py`, pick one **with a paid twin**, set `LARGE_MODEL` / `SMALL_MODEL` in `.env`, and update the two `model:` lines in `ex4_gateway/litellm_config.yaml`. Results are then not comparable with `results/` |
| `ledger is empty` from `to_focus.py` | the ledger is written by live runs; run Exercise 1 or 2a first, or use `--gateway` |
| `.../gateway_spend_logs.json not found` | run `run_teams.py --report` first, or pass `results/gateway_spend_logs_reduced.json` |
| `up.sh` hangs at "waiting for LiteLLM" / prints container logs and exits | first start runs DB migrations (we saw ~30 s; allow a few minutes). Check `docker logs finops-litellm` |
| `Postgres did not start (port 55432 busy? ...)` from `up.sh`, or port 4000 already in use | find it: `ss -ltnp \| grep -E ':4000\|:55432'`. Postgres: `PG_PORT=55433 ./ex4_gateway/up.sh`. LiteLLM's 4000 is fixed in `up.sh` (`--port 4000`) and `run_teams.py` (`LITELLM_BASE`): change both, e.g. `--port 4001` and `export LITELLM_BASE=http://127.0.0.1:4001` |
| `up.sh` fails with a container name conflict | `./ex4_gateway/down.sh` (it removes `finops-litellm` and `finops-pg`), then `up.sh` again |
| `docker: permission denied` | add your user to the `docker` group or run the scripts with `sudo`; only Exercise 4 needs Docker |
| Docker Desktop (macOS/Windows): gateway not reachable | `up.sh` uses `--network host`, which on Docker Desktop needs the host-networking option enabled in Settings (available since Docker Desktop 4.34; not tested by us) |
| `run_teams.py --setup` fails with `AssertionError (401, ...)` | the master key differs between `.env` and the running proxy: keep `LITELLM_MASTER_KEY` the same and restart with `up.sh` |
| `--traffic` never hits the budget | check that `--report` shows non-zero spend; if spend is $0 you are on the `openrouter/` route (see Exercise 4). Raise `--support-max` if some calls failed |
| Gateway spend is $0 for a model | the `openrouter/` pitfall above, or both prices set to 0 (LiteLLM then skips budgets by design) |
| `fastembed` install or model download fails | use `--lexical`; results for embeddings are in `results/semantic_cache_embeddings.md` |
| Different numbers from the tables above | expected: free models are non-deterministic and n=16. Compare trends (A vs B vs D, H vs I), not exact values |
