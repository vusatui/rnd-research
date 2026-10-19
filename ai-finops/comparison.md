# AI cost control: tools, gateways and approaches compared

State as read on **2026-10-19** (prices and plans change often; re-check the linked page before quoting).
Legend: ✅ verified on the vendor's page, 🟡 vendor claim, ❌ not verified, 🧪 tested in our workshop.

## 1. Where the cost controls sit

| Layer | What it gives you | Examples |
|---|---|---|
| Provider billing / cloud cost tools | the invoice, per-model/SKU lines, FOCUS export; weak per-feature attribution | OpenAI/Anthropic/Google consoles, AWS CUR + Bedrock attribution, Azure Cost Management |
| **LLM gateway** (single path for all calls) | attribution (key/team/tag), budgets, rate/token limits, model allow-lists, caching, fallbacks, logs | LiteLLM, Portkey (Prisma AIRS AI Gateway), Cloudflare AI Gateway, OpenRouter, Azure APIM, Kong, Envoy AI Gateway |
| Observability / tracing | tokens + computed cost per trace/span/user/feature, regression analysis | Langfuse, Phoenix, LangSmith, Helicone, Datadog |
| Application code | prompt design, context trimming, output caps, routing/cascades, validators, caching keys | your code, RouteLLM-style routers |

## 2. Gateways and attribution/budget features

| Product | License / price (2026-10-19) | Attribution | Budgets / limits | Notes |
|---|---|---|---|---|
| **LiteLLM proxy** 🧪 | OSS (MIT) free self-host; Enterprise (SSO, audit logs, some tag features) by sales ✅ [docs](https://docs.litellm.ai/docs/enterprise) | virtual keys, users, teams, request tags; spend logs in Postgres | max_budget + budget_duration per key/user/team; tag budgets; tpm/rpm limits; model allow-list per key/team ✅ [budgets](https://docs.litellm.ai/docs/proxy/users), [tag budgets](https://docs.litellm.ai/docs/proxy/tag_budgets) | 🧪 v1.106.0: team budget blocked at 112% (checked before the call); key-level `tags` 403 "Enterprise"; `openrouter/` free models logged $0 despite custom prices - used `openai/` + api_base instead; cost $0 = budgets bypassed by design ✅ |
| **Portkey / Prisma AIRS AI Gateway** | OSS gateway (MIT) ✅ [repo](https://github.com/Portkey-AI/gateway); platform: Developer free, Production $49/month, Enterprise custom ✅ [pricing](https://portkey.ai/pricing); acquired by Palo Alto Networks, completed 2026 ✅ [press](https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-portkey-to-secure-ai-agents) | metadata, virtual keys, user attribution | "Granular Budget & Rate Limits" listed under Enterprise ✅ | semantic cache on paid tiers; roadmap now tied to Palo Alto security portfolio 🟡 |
| **Cloudflare AI Gateway** | core features free on all plans (analytics, caching, rate limiting) ✅ [pricing](https://developers.cloudflare.com/ai-gateway/reference/pricing/); Unified Billing adds a credit fee ✅ | custom metadata on requests | spend limits by model/provider/metadata, returns 429; eventually consistent - may overshoot ✅ [spend limits](https://developers.cloudflare.com/ai-gateway/features/spend-limits/) | caching for identical requests only ✅ |
| **OpenRouter** 🧪 | no markup on inference; 5.5% fee on credit purchases (Standard), BYOK free to $25k/month then 5% ✅ [pricing](https://openrouter.ai/pricing) | per API key / workspace; cost returned in each response ✅ | key/workspace spend limits on paid plans ✅ | free tier 20 rpm, 50/day (1,000/day with ≥$10 credits) ✅; `openrouter/auto` router no extra fee ✅ |
| **Azure API Management** | APIM tier pricing (not compared here) | subscription key, IP or custom counter key | `llm-token-limit`: tokens/min (429) and token quota hourly..yearly (403), optional prompt estimate; per-gateway counters ✅ [docs](https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy) | `llm-emit-token-metric` for chargeback dashboards ✅ |
| **AWS Bedrock native attribution** | no extra charge noted ❌ | IAM principal attribution, application inference profiles + cost allocation tags, request metadata ✅ [best practices](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-best-practices.html) | via AWS Budgets / quotas | activation not retroactive; recommends a gateway to stamp tags ✅ |
| **Kong AI Gateway** | Kong licence tier not checked ❌ | consumers / consumer groups | AI Rate Limiting Advanced: limits by tokens or by computed **cost** ✅ [docs](https://developer.konghq.com/ai-gateway/policies/ai-rate-limiting-advanced/) | also semantic cache policy ✅ |
| **Envoy AI Gateway** | OSS (Apache-2.0) ✅ [repo](https://github.com/envoyproxy/ai-gateway) | Envoy/Kubernetes identities | token-based rate limiting ✅ | Kubernetes-native; fits teams already on Envoy Gateway |

Decision rule of thumb: start with whatever gateway the platform team can operate (LiteLLM for self-hosted
multi-provider, the cloud's native gateway if you are single-cloud), make it the **only** path to model APIs, and test
its budget enforcement and price table yourself before trusting its numbers.

## 3. Observability / cost tracking

| Tool | Price (2026-10-19) | Cost features |
|---|---|---|
| Langfuse | OSS self-host free; Cloud Hobby free (50k units), Core $29/month, Pro $199/month ✅ [pricing](https://langfuse.com/pricing) | cost from ingested usage or model price definitions, per trace/user/session ✅ [docs](https://langfuse.com/docs/observability/features/token-and-cost-tracking) |
| OpenTelemetry GenAI semconv | open standard (Development status) | token usage attributes; no standard cost attribute (see previous topic) ✅ |
| Provider usage fields | free | OpenRouter `usage.cost` ✅; OpenAI `cached_tokens`, `cache_write_tokens` ✅ |
| FOCUS 1.4 / 1.5 draft | open spec | 1.5 adds ModelId, TokenDirection, TokenCacheAction, PrincipalId/CredentialId ✅ [scope](https://focus.finops.org/focus-1-5-release-scope/) |

## 4. Provider price levers (per 1M tokens, 2026-10-19) ✅

| | OpenAI gpt-6.1-sol | OpenAI gpt-6-luna | Claude Sonnet 5.5 | Claude Haiku 5.5 | Gemini 4 Argon |
|---|---|---|---|---|---|
| Input / output | $2 / $10 | $0.10 / $0.50 | $2 / $10 | $0.10 / $0.50 (≤100K prompt) | $2 / $10 until 30 Nov 2026, then $4 / $20 |
| Cache read | $0.10 (0.05x) | $0.01 | 0.05x | 0.10x | $0.10 (implicit) |
| Cache write | $2.50 (1.25x) | $0.125 | 1.25x (5 min) / 2x (1 h) | 1.25x / 2x | none (implicit) |
| Batch | -50% (24h) | -50% | -50% | -50% | -50% (also Flex) |
| Premium speed | Fast 2x, Ultrafast 6x | - | Fast mode premium | - | Priority 1.8x |
| Other | >272K input 2x; residency +10% | | US-only inference 1.1x | >100K prompt 5x | output includes thinking tokens |

Sources: [OpenAI pricing](https://platform.openai.com/docs/pricing), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing),
[Anthropic caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing).

## 5. Cost levers: when to use which

| Lever | Expected saving | Effort | Quality risk | Use when | Workshop result 🧪 |
|---|---|---|---|---|---|
| Output caps + concise format | 20-30% where output dominates | low | low-medium (truncation) | chatty answers, JSON outputs | -26%, quality 14→15/16 |
| Context trimming / RAG top-k | proportional to removed input | medium | retrieval misses | stuffed "whole KB" prompts | -68%, 15/16 |
| Stable prefix + prompt caching | up to ~90% of cached input | low | none (same tokens) | repeated system prompts/tools, agent loops; ≥1-4K prefix | 0 vs 6,288 cached tokens/request |
| Smaller model | 80-95% | low | task-dependent | classification, extraction, templated replies | -96%, 14/16 |
| Cascade with validator | between small and large | medium | depends on validator | mixed difficulty traffic | confidence-only 13/16; +grounding 14/16 at -95% |
| Exact-match response cache | 100% per hit | low | stale answers | repeated identical requests | not run |
| Semantic cache | 100% per hit | medium | wrong answers on near-misses | FAQ-like traffic with validation | 9/12 near-misses would be served wrong at 0.80 |
| Batch / Flex | 50% | low-medium | latency only | evals, backfills, nightly jobs | not run |
| Prompt compression | up to 20x input (paper) | medium | task-specific | long retrieved docs, not cacheable prefixes | not run |
| Distillation / fine-tune | large at volume | high | drift, eval cost | high-volume narrow task | not run |
| Self-host | depends on utilization | high | ops | steady high load, residency needs | break-even 64% (vs open API) / 18% (vs frontier) on stated assumptions |
| Budgets / quotas / allow-lists | caps the tail | low | false blocks | every production key | blocked at 112% of budget; allow-list 403 |
