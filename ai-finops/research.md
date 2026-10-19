# AI cost control (FinOps for AI, token cost engineering) - research notes

The typical enterprise ask: *"Our LLM bill exploded. Tell us who is spending it, on what, and cut it without breaking
quality."* This document collects what is actually known (as of 2026-10-19) about why AI spend surprises
organizations, what the FinOps community recommends, which engineering levers move the bill, and how to attribute
and cap spend. Every important claim has a link; numbers we measured ourselves are marked 🧪 and come from
[`workshop/`](workshop/) (details: [`workshop-plan.md`](workshop-plan.md)).

All sources were checked on **2026-10-19** unless noted. Legend (same as the other topics):
- ✅ **verified**: read on the primary page (spec, vendor docs/pricing page, press release, paper, repo).
- 🟡 **vendor-claim / survey**: a vendor or consultancy talking about itself, its customers or its own survey; not reproduced.
- 🟠 **secondary**: blogs, aggregators, price indexes; primary data not read by us.
- 🔮 **forecast**: an analyst prediction, not a fact.
- ❌ **unverified / disputed**.
- 🧪 **measured by us** in the workshop (free OpenRouter models, shadow-priced; n=16 tickets per configuration).

Prices change monthly. Every price below is "as read on 2026-10-19" from the linked page; re-check before quoting.

## TL;DR (key findings)

1. **Cheaper tokens, bigger bills.** Price per unit of capability falls fast (Epoch AI: ~13x per year for a fixed
   performance level, 2023-2026 ✅), but consumption grows faster: agents re-send context on every step, call
   sub-agents, retry, and reason. Gartner predicts inference cost *per agentic workflow* will rise more than fivefold
   through 2028 🔮; Accenture's survey finds 9 in 10 executives would spend price cuts on new use cases, not savings 🟡.
   The client conversation therefore has to move from "price per token" to **cost per successful task**.
2. **FinOps for AI is now mainstream FinOps.** 98% of 1,192 State of FinOps 2026 respondents manage AI spend (31% two
   years earlier) and FinOps for AI is the top forward-looking priority ✅. The FinOps Foundation's guidance is
   pragmatic: Price x Quantity still applies, tag/allocate per use case, set quotas and anomaly detection, track
   cost per inference / per token / per API call and tie it to business value ✅.
3. **Billing data is getting a common shape.** FOCUS 1.4 (published, June 2026) is the open billing schema all major
   clouds emit; FOCUS 1.5 (working draft, ratification planned 3 Dec 2026) adds exactly what AI chargeback needs:
   model identity, cached vs uncached and input vs output token labels, and **who** made the call (PrincipalId /
   CredentialId) ✅. Today, attribution still has to be stamped by your own gateway.
4. **The levers are known; their size depends on the workload.** In our ticket-reply workshop (same 16 tickets,
   frontier price card) 🧪: concise output -26% cost with *better* quality (15/16 vs 14/16); context trimming -68%
   (15/16); a small model -96% (14/16); small model on trimmed context -98% but quality collapsed (9/16). A cascade is
   only as good as its validator: a self-reported-confidence check escalated 1 of 16 and let a hallucinated
   Enterprise price through; adding a 10-line "every $ amount must exist in the knowledge base" check caught it
   (14/16 at -95%).
5. **Prompt caching is the biggest "free" lever - if the prefix is stable.** Providers now converge on
   write 1.25x / read 0.10x (OpenAI GPT-5.6+, Anthropic 5-min) or cheaper reads (0.05x on some models; Gemini implicit
   caching with no write fee) ✅. One dynamic value (timestamp, request id) at the top of the prompt turns every
   request into a paid cache write that is never read. Measured: with an ~8k-token prompt, the stable-prefix variant got
   6,288 cached tokens per request from the 2nd request on; the dynamic-prefix variant got 0 🧪.
6. **Semantic caching is a quality risk, not just a saving.** Near-miss questions ("Business plan" vs "Enterprise
   plan", "export" vs "import") score *higher* similarity than true paraphrases with a common embedding model 🧪,
   consistent with vCache (ICLR 2026): correct and incorrect hits overlap (mean similarity 0.85 vs 0.84) ✅.
7. **Budgets need a gateway, and gateways need checking.** Self-hosted LiteLLM enforced a per-team budget and a model
   allow-list in our run 🧪, but (a) the budget check happens before the request, so the team ended at 112% of budget;
   (b) with the `openrouter/` provider prefix our custom prices were silently ignored ($0 logged), so budgets never
   tripped until we switched provider type (root cause, traced in the v1.106.0 source and reproduced: the OpenRouter
   integration copies OpenRouter's own `usage.cost`, 0 for `:free` models, into the response cost, which takes precedence
   over custom prices 🧪); (c) key-level tags are an Enterprise feature. Cloudflare documents the same
   eventual consistency for its spend limits ✅. Verify gateway cost numbers against a hand calculation.
8. **Self-hosting wins only at high, steady utilization.** The break-even is a utilization question: with our
   assumptions (8xH100 at $3.50/GPU-h, 5,000 tok/s, $15k/month ops) a replica must run at ~64% average utilization to
   beat an open-weights model bought via API, ~18% to beat a frontier API price 🧪 (arithmetic on stated assumptions,
   not a benchmark). Business-hours-only traffic caps an always-on replica at ~30%.

## 1. Why AI spend surprises clients

### 1.1 Demand signals
- **State of FinOps 2026** (FinOps Foundation / Linux Foundation, 19 Feb 2026, 1,192 respondents, >$83B cloud
  spend): 98% manage AI spend, up from 31% two years ago; FinOps for AI is the top forward-looking priority; "AI value
  management" is the #1 skillset teams want; many organizations are asked to **self-fund AI through efficiency
  gains**; pre-deployment architecture guidance ("shift left") is a top desired capability ✅
  [press release](https://www.linuxfoundation.org/press/state-of-finops-survey-ai-value-and-skills-top-priorities-as-finops-matures-across-technology-value-98-manage-ai-90-saas-64-licensing-48-data-center-1).
- **Services market**: EPAM's Q2 2026 earnings call lists "token cost engineering" among the AI-native engineering
  offerings, and says some client spend is shifting from services to "tokens, hardware and infrastructure" 🟡
  [transcript](https://www.fool.com/earnings/call-transcripts/2026/08/06/epam-epam-q2-2026-earnings-call-transcript/).
- **McKinsey** (14 Oct 2026, expert interview): moving an AI tool from pilot to production "can nearly quadruple its
  cost"; in 2026 providers moved to consumption-based pricing; by April-May 2026 executives saw "a single user could
  rack up thousands of dollars in a single day"; a poorly designed agent can use "up to 30 times as many tokens" 🟡
  (expert opinion, no published dataset) [article](https://www.mckinsey.com/featured-insights/mckinsey-explainers/what-does-ai-really-cost).
- **Accenture** CIO tokenomics survey: surveyed enterprises spent ~$2.5B on tokens last year; expected consumption
  +78% in 24 months; ~$3.6B spend even after a predicted 19% price decline; 9 in 10 executives say cheaper tokens lead
  to more use cases; 1 in 20 would bank a 25% price cut; anecdotes of 5-10x token-spend growth in six months 🟡
  [report](https://www.accenture.com/en/insights/ai-data/cios-guide-ai-tokenomics).
- **EY**: the cost of an agent has seven categories; most business cases include only the first three (tokens/API,
  subscriptions/licences, infrastructure), the rest (e.g. orchestration, observability, governance, human review)
  appear later 🟡 [article](https://www.ey.com/en_us/insights/ai/agentic-ai-token-costs).

### 1.2 Mechanisms (why the bill grows faster than usage looks)
- **Statelessness**: every agent step re-sends instructions, tool definitions, history and tool results; cost grows
  with steps x context, not with user messages (McKinsey interview above 🟡; OpenAI caching guide discusses the same
  growing-prefix pattern ✅ [docs](https://platform.openai.com/docs/guides/prompt-caching)).
- **Output is the expensive side**: output tokens cost 5x input on current flagship price cards (gpt-6.1-sol
  $2/$10, Claude Sonnet 5.5 $2/$10 per 1M) ✅ [OpenAI](https://platform.openai.com/docs/pricing),
  [Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). Reasoning ("thinking") tokens are
  billed as output (e.g. Gemini: "Output price (including thinking tokens)") ✅
  [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing).
- **Price cliffs and multipliers** that are easy to miss ✅:
  - long-context tiers: OpenAI prices >272K-token requests at 2x input (gpt-6.1-sol $4 vs $2); Claude Haiku 5.5
    costs 5x above 100K-token prompts ([OpenAI](https://platform.openai.com/docs/pricing),
    [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing));
  - data residency: +10% (OpenAI regional endpoints for models released from 5 Mar 2026; Anthropic `inference_geo:
    "us"` 1.1x);
  - speed tiers: OpenAI "Fast" (renamed from Priority on 30 Jul 2026) is 2x standard, "Ultrafast" 6x on gpt-6.1-sol;
    Gemini Priority 1.8x; discounted tiers: Batch and Flex 50% (OpenAI, Gemini), Batch 50% (Anthropic)
    ([OpenAI](https://platform.openai.com/docs/pricing), [Gemini](https://ai.google.dev/gemini-api/docs/pricing),
    [Anthropic batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing)).
- **Promotional pricing ends**: Gemini 4 Argon is $2/$10 per 1M "through November 30, 2026" and $4/$20 from
  1 Dec 2026; OpenAI notes GPT-5.6 Sol promotional pricing "at least through November 21, 2026" ✅
  ([Gemini](https://ai.google.dev/gemini-api/docs/pricing), [OpenAI](https://platform.openai.com/docs/pricing)).
  A forecast built on promo prices doubles overnight. The FinOps Foundation explicitly warns about cost increases
  after preview/free phases ✅ [FinOps for AI overview](https://www.finops.org/wg/finops-for-ai-overview/).
- **Free models hide the problem**: free tiers cost $0, so nobody sees the bill until migration to a paid endpoint.
  Gateways treat $0 as "not budgeted": LiteLLM documents setting costs to 0 as the way to let free/on-prem models
  **bypass budget checks** ✅ [LiteLLM custom pricing](https://docs.litellm.ai/docs/proxy/custom_pricing). Our workshop prices every free call at
  its paid twin's list price ("shadow cost").
- **Gartner** (17 Aug 2026): inference cost per agentic workflow will increase more than fivefold through 2028;
  "Product leaders cannot rely on more efficient token economics to rationalize AI costs" 🔮
  [press release](https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028).

## 2. FinOps Foundation guidance and FOCUS

### 2.1 FinOps for AI (Working Group papers)
[FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/) (last updated 17 Feb 2026) ✅:
- "Basic Price x Quantity = Cost equation still applies": reduce rate (commitments, tiers) or quantity (tokens).
- What differs for AI: inconsistent and fast-changing pricing ("may change wildly up or down"), new SKUs without native
  tagging, tokens as meters (the prompt the user typed is not the prompt that is billed), GPU scarcity, immature
  engineering practice, and allocation of a shared model across many features ("tech support chatbot" vs "new customer
  chatbot") with "lack of generally accepted frameworks for cost allocation across multi-agent workloads".
- Practices: showback before chargeback, tagging (example keys Project/Environment/Workload/Team/CostCenter/...),
  usage limits, quotas, throttling and anomaly detection, prompt optimization and caching, distillation/quantization,
  batching for non-real-time work, commitments (e.g. provisioned throughput) for predictable load.
- Crawl / walk / run: manual estimates and fail-fast limits in pilots; basic automation and anomaly analysis when
  integrated; automated tracking, advanced anomaly detection and ROI-level metrics in production.
- KPIs: cost per inference, cost per token, cost per API call, resource utilization, anomaly rate, ROI, time to value,
  and a "model choice quality score" (is the model more capable - and expensive - than the task needs?).

Other Working Group papers used: [How to Build a Generative AI Cost and Usage Tracker](https://www.finops.org/wg/how-to-build-a-generative-ai-cost-and-usage-tracker/)
(token-level tracking, centralized hub-and-spoke vs decentralized, provisioned-throughput allocation) ✅,
[Effect of Optimization on AI Forecasting](https://www.finops.org/wg/effect-of-optimization-on-ai-forecasting/)
(model selection, backend infrastructure and consumer-side optimizations change forecasts; link cost-per-unit-of-work
to value) ✅, [Unlocking AI Business Value](https://www.finops.org/wg/unlocking-ai-business-value-with-finops/)
(value vs feasibility rubric per use case) ✅.

### 2.2 FOCUS (FinOps Open Cost and Usage Specification)
- **FOCUS 1.4** ratified/announced June 2026: adds Invoice Detail and Billing Period datasets, 47 columns, invoice
  reconciliation and commitment-eligibility features; no incompatible changes ✅
  [changelog](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/blob/v1.4/CHANGELOG.md),
  [announcement](https://www.finops.org/insights/introducing-focus-1-4/). All major clouds generate FOCUS data natively;
  ~68% of $100M+ spenders use or experiment with it (State of FinOps 2026) ✅.
- **AI today**: FOCUS already carries tokens (ConsumedQuantity/ConsumedUnit, SkuId, ServiceCategory "AI and Machine
  Learning", credits via PricingCurrency) ✅ [FOCUS for AI](https://focus.finops.org/technology-categories/focus-for-ai/);
  practitioners still lacked worked examples ("We work with over 20 vendors for AI providers, and every single one has
  a different data format") ✅ [FR #1941](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/issues/1941).
- **FOCUS 1.5** (working draft; ratification planned **3 Dec 2026**; page updated Oct 2026) ✅
  [release scope](https://focus.finops.org/focus-1-5-release-scope/):
  - SKU Price Details properties `ModelDeveloper`, `ModelFamily`, `ModelId`, `ModelVersion` (recommended);
  - `TokenCacheAction` (Uncached / Read / Write / Other) and `TokenDirection` (Input / Output); reasoning tokens are
    "Output"; example queries for cache hit rate by model;
  - new Cost and Usage columns `PrincipalId`, `CredentialId`, `RequesterDetails` - "which developer, service, or agent
    made the call", never the key string itself; note: they do *not* say who *benefits* (a gateway acting for many users);
  - a SKU Price dataset (price catalog, in final review), six worked AI billing scenarios, consumption currencies;
  - *not* in 1.5: reasoning tokens billed but not returned, context-cache storage fees, modality, context-window
    pricing, priority/batch tiers, provisioned throughput as commitment, agentic subcategories.
- Implication: until providers emit 1.5 data, attribution by team/feature/agent comes from **your gateway logs**, which
  you can already shape like FOCUS (our `to_focus.py` does this; not validated with the FOCUS validator 🧪).

## 3. Unit economics: cost per task, not per token
- FinOps Foundation: cost per inference / per API call / per token, and "cost-per-call, time-to-close, customer
  satisfaction score divided by AI costs" for customer service ✅ [overview](https://www.finops.org/wg/finops-for-ai-overview/).
- McKinsey interviewees: "It's not just about cost per token. It's about cost per task." 🟡
- We recommend (and the workshop computes) three numbers per feature: **$ per task**, **$ per successful task**
  (= $/task / pass rate, so a cheap but wrong configuration is penalized) and **$ per month at forecast volume** 🧪.
  Example from our run (frontier price card, 100k tickets/month): baseline $1,250/month at 14/16 pass; trimmed context
  on the same model $394 at 15/16; small model $46 at 14/16 🧪.

## 4. Token cost levers

| Lever | Typical size (source) | Main risk | Our measurement 🧪 |
|---|---|---|---|
| Output length control (instructions + max_tokens) | proportional to output share; output costs 5x input on flagship cards ✅ | truncation, missing facts | -26% cost, 403 → 85 output tokens, quality 14 → 15/16 |
| Context trimming / retrieval | proportional to input share | retrieval misses → wrong answers | -68% (4.2k → 1.5k input tokens), 15/16; BM25 recall@3 was 14/16 |
| Model routing / cascade | RouteLLM: >2x savings at near-GPT-4 quality, benchmark-dependent (3.66x MT-Bench, 1.4-1.5x MMLU/GSM8K) ✅; FrugalGPT: up to 98% on one dataset ✅ | small model hallucinations; weak escalation signal | small model -96% at 14/16; cascade with confidence check escalated 1/16 (13/16); with number-grounding check 14/16 at -95% |
| Prompt caching | reads 0.05-0.10x, writes 1.0-2.0x by provider ✅ | dynamic prefix = paid writes never read; TTL; min length | 0 vs 6,288 cached tokens/request (dynamic vs stable, ~8k prompt); hits on ~4k prompts were sporadic (0-15%) |
| Semantic caching | vendor-dependent; vCache: thresholds can't separate correct/incorrect hits ✅ | wrong answers served at zero cost | near-misses scored higher than paraphrases (mean 0.836 vs 0.824) |
| Batch / Flex tiers | 50% off, async (OpenAI 24h window, Anthropic, Gemini) ✅ | latency; not for interactive flows | not measured (no batch API on the free tier); applies to evals, backfills, nightly jobs |
| Prompt compression | LLMLingua: up to 20x with 1.5-point drop on GSM8K; 25-30x degrades ✅ | task-specific loss | not measured |
| Distillation / fine-tuned small models | 770M T5 beat few-shot 540B PaLM on two benchmarks with 80% of data (Distilling step-by-step) ✅ | training + eval cost, drift | not measured |
| Self-hosting | utilization-driven (see §6) | idle GPUs, ops cost | arithmetic only |
| Budgets, quotas, allow-lists | prevent runaway spend rather than reduce unit cost | overshoot, false blocks | budget tripped at 112%; model allow-list 403 |

### 4.1 Model routing and cascades
- **RouteLLM** (LMSYS/Berkeley, 2024): routers trained on preference data between a strong and a weak model; ">2x"
  cost reduction without quality loss on MT-Bench-like traffic, but gains are benchmark-specific and the best results
  used data augmentation matched to the benchmark ✅ [arXiv 2406.18665](https://arxiv.org/abs/2406.18665).
- **FrugalGPT** (Stanford, 2023): LLM cascade with a learned answer scorer; "up to 98.3%" cost reduction while
  matching GPT-4 on HEADLINES; other datasets 59-73% ✅ [arXiv 2305.05176](https://arxiv.org/abs/2305.05176).
- Commercial routers exist (OpenRouter `openrouter/auto` "adds no fee" ✅ [pricing FAQ](https://openrouter.ai/pricing);
  LiteLLM "Auto Router" ✅ [docs](https://docs.litellm.ai/)), but their quality on *your* traffic must be measured.
- 🧪 Lesson: the escalation signal is the product. Self-reported confidence was ≥0.75 on 15/16 small-model answers,
  including one with an invented price. A deterministic grounding check is cheap and caught it. (This connects to the
  `system-one-models` topic: calibrated small classifiers as routers.)

### 4.2 Prompt caching (provider semantics, read 2026-10-19) ✅
| Provider | How | Write | Read | Min prefix | Lifetime |
|---|---|---|---|---|---|
| OpenAI GPT-5.6+ | implicit (end of latest eligible message) or explicit breakpoints (`prompt_cache_options`), up to 4 writes/request | 1.25x | 0.10x (0.05x gpt-6.1-sol) | 1,024 visible tokens | ≥30 min after last write/reuse |
| OpenAI ≤5.5 | implicit, `prompt_cache_key` helps routing | none | model-dependent | varies | 5-10 min in-memory or 24h retention |
| Anthropic | `cache_control` breakpoints or automatic | 1.25x (5 min), 2x (1 h) | 0.10x (0.05x Opus/Sonnet 5.5, 0.025x Fable/Mythos 5.1) | 512-4,096 by model | 5 min refreshed on use, or 1 h |
| Gemini | implicit (automatic); see docs for explicit caching | none (implicit) | e.g. $0.10 vs $2.00 input on Gemini 4 Argon | 2,048-4,096 | best effort |
| OpenRouter | passes provider caching through, sticky routing to keep caches warm (10 min) | per provider | per provider | per provider | per provider |

Sources: [OpenAI caching](https://platform.openai.com/docs/guides/prompt-caching),
[Anthropic caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching),
[Gemini caching](https://ai.google.dev/gemini-api/docs/caching), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing),
[OpenRouter caching](https://openrouter.ai/docs/guides/best-practices/prompt-caching).

Practical rules (all from the provider docs): stable content first, dynamic content last; append, don't rewrite
history; keep tool definitions and order stable (`tool_choice:"none"` instead of removing tools); compaction and
summarization reset the prefix; cached tokens still count toward rate limits (OpenAI); OpenAI documents a
"minimum cacheable length cost trap" for prefixes just under the threshold. Caching also has a **privacy angle**:
OpenAI recommends per-customer `prompt_cache_key` partly to prevent cache-hit probing across users ✅.

🧪 Our simulation on the measured prompt shape (4,173-token stable prefix + ~45 per ticket): with a 1.25x write premium
a cache that is written once and never read costs **1.25x** (more than no caching); at 5 requests per TTL window
0.34x; at 100 requests 0.12x (OpenAI GPT-5.6+/Anthropic 5-min rules) - see `results/caching_sim_C_stable.md`.

### 4.3 Semantic caching
- vCache (ICLR 2026): on 45,000 samples the similarity distributions of correct and incorrect cache hits overlap
  (means 0.85 vs 0.84); optimal thresholds vary per cached item from 0.71 to 1.0, so a single global threshold cannot
  guarantee correctness; they learn per-embedding thresholds with a user-set error bound ✅
  [arXiv 2502.03771](https://arxiv.org/abs/2502.03771).
- Gateways ship it as a feature (Portkey lists "Simple & Semantic Caching" on paid tiers ✅ [pricing](https://portkey.ai/pricing));
  Cloudflare AI Gateway caches only identical requests (semantic "planned") ✅ [caching](https://developers.cloudflare.com/ai-gateway/features/caching/).
- 🧪 bge-small-en-v1.5 on 24 hand-made pairs: at threshold 0.80 a semantic cache would save 8/12 paraphrase calls and
  serve 9/12 wrong answers; "Business plan" vs "Enterprise plan" scored 0.946. The pairs were deliberately built as
  near-misses, so this is a stress test, not a traffic estimate. Use exact-match caching for safe wins; semantic
  caching only with per-domain validation, short TTLs and no caching for account-specific or numeric answers.

### 4.4 Other levers (brief)
- **Batch / Flex**: 50% discount for asynchronous work; OpenAI batches complete within 24h ✅
  [OpenAI batch](https://platform.openai.com/docs/guides/batch); stacks with caching on Anthropic ✅.
- **Prompt compression**: LLMLingua up to 20x with small loss on reasoning benchmarks; degrades at 25-30x ✅
  [arXiv 2310.05736](https://arxiv.org/abs/2310.05736). Note it competes with caching (a compressed prompt that changes
  per request is not cacheable).
- **Distillation**: Distilling step-by-step ✅ [arXiv 2305.02301](https://arxiv.org/abs/2305.02301); the FinOps
  Foundation lists distillation, pruning and quantization as model optimization ✅.
- **Rate tier selection**: Flex/Batch for tolerant work, avoid Fast/Priority by default; data residency +10%.

## 5. Attribution, budgets and gateways
- The FinOps Foundation's allocation challenge for AI is identifying the *consumer* of a shared model ✅. AWS's
  guidance is the clearest vendor statement of the architecture: stamp attribution "in a shared client wrapper or LLM
  gateway", restrict the call path so the gateway is the only route (SCPs/IAM), use low-cardinality tags for billing
  and high-cardinality ids only in request logs, never put PII in tags, reconcile log-derived cost against the invoice ✅
  [Bedrock cost attribution best practices](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-best-practices.html).
- Native cloud options ✅: Bedrock IAM principal attribution, application inference profiles with cost-allocation tags,
  per-request metadata (16 entries) [docs](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-application-inference-profiles.html);
  Azure API Management `llm-token-limit` (per-key tokens-per-minute 429, token quota per hour..year 403; counts are
  per gateway, concurrent requests can exceed the limit) and `llm-emit-token-metric`
  [docs](https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy).
- Gateways (details and prices in [`comparison.md`](comparison.md)): LiteLLM (OSS, budgets per key/user/team, tag
  spend tracking), Portkey (acquired by Palo Alto Networks in 2026, now "Prisma AIRS AI Gateway"; OSS gateway plus
  paid platform) ✅ [press](https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-portkey-to-secure-ai-agents),
  Cloudflare AI Gateway (spend limits per model/provider/metadata, eventually consistent) ✅
  [docs](https://developers.cloudflare.com/ai-gateway/features/spend-limits/), OpenRouter (budgets per key/workspace,
  no inference markup, 5.5% credit fee) ✅ [pricing](https://openrouter.ai/pricing), Kong and Envoy AI Gateway
  (token/cost-based rate limiting) ✅ [Kong](https://developer.konghq.com/ai-gateway/policies/ai-rate-limiting-advanced/),
  [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway).
- 🧪 What we saw with LiteLLM v1.106.0 (self-hosted): team budget + model allow-list work; overshoot by one request;
  team spend lags one request; key-level tags need Enterprise; `openrouter/` prefix logged $0 despite custom prices.

## 6. Self-hosting vs API
- The FinOps Foundation frames the choice as infrastructure strategy with utilization as a KPI ✅
  [overview](https://www.finops.org/wg/finops-for-ai-overview/),
  [Choosing an AI approach](https://www.finops.org/wg/choosing-an-ai-approach-and-infrastructure-strategy/).
- GPU prices: H100 on-demand at specialist clouds is roughly $3.5-4/GPU-hour, hyperscaler list ~ $10 (Oct 2026) 🟠
  [GPU Economy index](https://gpueconomy.com/price-index), [GetDeploying](https://getdeploying.com/gpus/nvidia-h100).
- Published break-even analyses (blogs) put the required sustained utilization of a rented 2xH100 open-model server
  at 72% sustained utilisation vs a serverless endpoint (gpt-oss-120b, $4,803/month) 🟠 [example](https://www.francisokafor.com/field-notes/self-hosted-open-weights-break-even-utilisation).
- 🧪 Our calculator (`ex5_breakeven/breakeven.py`) makes every assumption explicit: fixed cost = GPUs x $/h x 730 +
  ops; capacity = throughput x hours x utilization. Default result: 64% utilization to beat $0.60/$2.40 (open model via
  API), 18% to beat $2/$10 (frontier price). At hyperscaler GPU prices ($10/h) the first becomes impossible (>100%).
  Throughput (5,000 tok/s per 8-GPU replica) is an **assumption**, not a measurement.
- Non-cost reasons dominate many self-hosting decisions (data residency, latency, model control); price them
  separately.

## 7. Observability of cost
- OpenTelemetry GenAI conventions carry token usage but, as found in the previous topic, no standard cost attribute ✅
  (see [`../agents-pilot-to-prod/research.md`](../agents-pilot-to-prod/research.md)); cost is computed downstream from a
  price table (Langfuse does this with model price definitions ✅
  [docs](https://langfuse.com/docs/observability/features/token-and-cost-tracking)).
- OpenRouter returns cost and cached-token counts in every response ✅
  [usage accounting](https://openrouter.ai/docs/guides/guides/usage-accounting); OpenAI exposes `cached_tokens` and
  `cache_write_tokens` ✅. Track **cache hit rate by model** - FOCUS 1.5 adds exactly this example query.
- The FinOps Foundation recommends anomaly detection against historical baselines ("if token consumption doubles
  without clear justification...") ✅.

## 8. Pricing trends
- Epoch AI (Mar 2025): price to reach a fixed benchmark level fell 9x-900x per year depending on task, median 50x;
  faster after Jan 2024 ✅ [data insight](https://epoch.ai/data-insights/llm-inference-price-trends).
- Epoch AI ("The plunging price of thought"): ~47% per quarter (~13x per year) since 2023, faster right after a level
  becomes state of the art (75x/yr) and slower two years later (4.7x/yr); caveats: benchmark gaming, users don't switch
  models as often as the frontier analysis assumes ✅ [publication](https://epoch.ai/publications/the-plunging-price-of-thought).
- Counter-trend: new top tiers are priced *higher* (gpt-6-astra $10/$50; Claude Fable 5.1 $10/$50 per 1M) and
  promos expire (Gemini 4 Argon doubles on 1 Dec 2026) ✅. Per-workflow cost rising (Gartner 🔮).

## 9. Consensus vs disputed

**Consensus**
- Measure and allocate at the use-case level; unit cost per task tied to value (FinOps Foundation, McKinsey, EY).
- Put a gateway or shared client in the path to stamp attribution and enforce limits (AWS guidance, FinOps WG).
- Stable-prefix prompt caching and batch tiers are low-risk savings where the workload fits (provider docs).
- Do not use the most capable model by default; match model to task (FinOps "model choice quality score").

**Disputed / uncertain**
- Will falling token prices fix budgets? Epoch shows steep declines; Gartner, Accenture and McKinsey interviewees
  argue consumption (Jevons) outruns them. Both can be true: unit price down, bill up.
- Routing/cascade savings in production: research numbers are benchmark-specific (RouteLLM authors note it); our
  n=16 run shows quality depends on the escalation signal.
- Semantic caching safety (vCache vs vendor marketing of semantic caches).
- Self-hosting economics: published break-evens vary by an order of magnitude with throughput and utilization
  assumptions; most are blogs.
- Whether "token cost engineering" is a new discipline or FinOps + performance engineering under a new name.

## 10. What we did not verify / open items
- Survey numbers (Accenture, McKinsey interviews, EY categories) are self-reported by the publishers 🟡.
- GPU prices and published break-evens are secondary 🟠; our throughput figure is an assumption.
- We did not test Portkey, Cloudflare AI Gateway, Kong, Envoy AI Gateway, Azure APIM or Bedrock attribution hands-on -
  documentation only. We tested LiteLLM v1.106.0 OSS only.
- Provider caching on paid endpoints was not measured; our cache numbers come from a free endpoint whose caching is
  undocumented and sporadic; provider multipliers are applied by simulation.
- Batch APIs, prompt compression and distillation were not run.
- FOCUS export is shaped by hand from the 1.4 column library and the 1.5 *draft* property names; not validated.
- All workshop quality numbers: one free model pair, 16 tickets, one run per configuration. Treat differences of
  1-2 tickets as noise.
