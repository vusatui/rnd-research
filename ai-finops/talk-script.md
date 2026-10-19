# Talk script: "AI cost control: FinOps for AI and token cost engineering" (~35 min)

Working title from the outline: *Tokens got cheaper. Why did your AI bill go up?*
Audience: engineers and consultants working on enterprise AI projects.

25 slides, 35:00 of planned speaking time including Q&A. The HTML deck is in [`slides/index.html`](slides/index.html). Its speaker notes are built from this file by `slides/build_notes.py`, so edit the notes here first. Likely audience questions with prepared answers are at the end of this file.

**Facts policy.** Every fact comes from [`research.md`](research.md), [`comparison.md`](comparison.md), [`talk-outline.md`](talk-outline.md) and [`workshop-plan.md`](workshop-plan.md) (sources checked and our own runs on 2026-10-19), plus the code and outputs in [`workshop/`](workshop/). Markers follow `research.md` and [`../agents-pilot-to-prod/talk-script.md`](../agents-pilot-to-prod/talk-script.md): ✅ verified on a primary page (spec, vendor docs or pricing page, paper, press release), 🟡 vendor claim or survey (a vendor or consultancy talking about itself, its customers or its own survey; not reproduced), 🟠 secondary source only (blogs, price indexes), ❌ not published / unverified / disputed, 🧪 measured by us in the workshop, 🔮 forecast (we verified that the analyst said it, not that it will happen). Say 🟡/🟠/🔮/❌ items out loud as claims, not as facts.

**Measurement caveat (say it early, repeat it).** All 🧪 numbers come from one free model pair on OpenRouter (large = `nvidia/nemotron-3-ultra-550b-a55b:free`, small = `nvidia/nemotron-3.5-lightning:free`), **16 tickets, one run per configuration**, shadow-priced at published paid prices. A difference of 1-2 tickets in pass rate is noise. Cost differences are more robust than quality differences, because token counts are stable while pass/fail flips on single answers. We tested only LiteLLM v1.106.0 OSS as a gateway; everything about other gateways is from their docs. Prices change monthly; every price is "as read on 2026-10-19".

**Presenter keys (deck):** → / Space / PageDown next, ← / PageUp back, Home / End, `N` notes overlay, `S` speaker window (notes, next slide, timer), `O` overview, `F` fullscreen. Open with `?check` for the overflow report.

| # | Slide | Time | Ends at |
|---|---|---|---|
| 1 | AI cost control | 0:30 | 0:30 |
| 2 | Same 16 tickets: $1,250 or $46 a month | 1:30 | 2:00 |
| 3 | Cheaper tokens, bigger bills | 1:45 | 3:45 |
| 4 | Why the bill grows faster than usage looks | 1:30 | 5:15 |
| 5 | Price cliffs and multipliers | 1:30 | 6:45 |
| 6 | Numbers not to quote without context | 1:15 | 8:00 |
| 7 | FinOps for AI: the community playbook | 1:45 | 9:45 |
| 8 | FOCUS: billing data gets an AI shape | 1:30 | 11:15 |
| 9 | The unit metric: $ per successful task | 1:45 | 13:00 |
| 10 | The test subject: a ticket-reply pipeline | 1:00 | 14:00 |
| 11 | Lever lab: cost vs quality | 2:00 | 16:00 |
| 12 | Levers: research size vs our measurement | 1:45 | 17:45 |
| 13 | Levers interact, and n=16 is small | 1:15 | 19:00 |
| 14 | A cascade is only as good as its verifier | 1:30 | 20:30 |
| 15 | T11: the invented Enterprise price | 1:30 | 22:00 |
| 16 | Prompt caching: keep the prefix stable | 1:45 | 23:45 |
| 17 | When caching costs more than no caching | 1:15 | 25:00 |
| 18 | Semantic cache: cheap wrong answers | 1:30 | 26:30 |
| 19 | One path to the models: the gateway | 1:30 | 28:00 |
| 20 | What the gateway actually did | 1:30 | 29:30 |
| 21 | Self-host or API: a utilization question | 1:30 | 31:00 |
| 22 | Gateway landscape | 1:00 | 32:00 |
| 23 | What we did not verify | 1:00 | 33:00 |
| 24 | AI cost-control checklist | 1:15 | 34:15 |
| 25 | Questions? | 0:45 | 35:00 |

---

## Slide 1 — AI cost control
**Timing:** 0:30 (0:00–0:30)
**On slide:**
- Title: AI cost control: FinOps for AI and token cost engineering
- Subtitle: Tokens got cheaper. Why did your AI bill go up?
- Anton Vusatyi · R&D · October 2026
- Repo: github.com/vusatui/rnd-research → ai-finops

**Speaker notes:**
Hi, I'm Anton. This talk is about a request that shows up in almost every enterprise AI project once it leaves the pilot: the LLM bill exploded, tell us who is spending it, on what, and cut it without breaking quality. I will cover why AI bills surprise, what the FinOps community recommends, which engineering levers move the bill and what each one costs in quality, and how to attribute and cap spend. Sources were checked on October 19, 2026. Numbers marked with a test tube come from a small workshop we ran ourselves, and everything is in the public repo on the slide.

**Sources:** [README.md](README.md), [talk-outline.md](talk-outline.md)

## Slide 2 — Same 16 tickets: $1,250 or $46 a month
**Timing:** 1:30 (0:30–2:00)
**On slide:**
- Same 16 support tickets, same eval checks, projected to 100k tickets/month on a frontier price card 🧪
- A: large model, whole knowledge base, verbose → **$1,250/month**, 14/16 pass
- F: small model, same prompt, concise → **$46/month**, 14/16 pass
- G: small model + trimmed context → **$19/month** (-98%), but **9/16** pass: 7 of 16 answers wrong
- Question: which number does your CFO see, and which one does your customer see?
- Legend: ✅ verified · 🟡 vendor claim · 🟠 secondary · 🔮 forecast · ❌ not published · 🧪 measured by us

**Speaker notes:**
Let me start with a result from our own run. We built a small support-ticket reply pipeline for a fictional invoicing SaaS and ran the same 16 tickets through different configurations, checking every answer with the same automatic checks.

Configuration A is what a first pilot usually looks like: the large model, the whole knowledge base pasted into the prompt, and a request for a thorough, warm reply. Priced at a frontier list price and projected to 100,000 tickets a month, that is about 1,250 dollars a month, with 14 of 16 tickets passing. Configuration F uses a small model and a concise answer format: 46 dollars a month, also 14 of 16.

And then configuration G stacks one more saving, trimming the context, and gets to 19 dollars a month, 98 percent cheaper. But only 9 of 16 pass. Seven customers get a wrong answer.

So the question for the next half hour: which of these numbers does your CFO see, and which does your customer see? A cost number without a quality number next to it is not a result.

One honest note up front: this is 16 tickets, one run each. I will come back to what that means. The legend at the bottom is the one I use on every slide: green verified, yellow vendor or survey claim, orange secondary, crystal ball forecast, red not published, test tube measured by us.

**Sources:** [workshop-plan.md](workshop-plan.md) (Block 1, measured 2026-10-19), [workshop/results/levers_summary_A-H.md](workshop/results/levers_summary_A-H.md), [workshop/app/pipeline.py](workshop/app/pipeline.py)

## Slide 3 — Cheaper tokens, bigger bills
**Timing:** 1:45 (2:00–3:45)
**On slide:**
- Diagram (schematic, not data): price per token for a fixed capability falls; tokens per task and the bill rise
- Epoch AI: price for a fixed capability level falls ~47% per quarter (~13x/year) since 2023 ✅; across tasks 9x-900x/yr, median 50x ✅
- Gartner (17 Aug 2026): inference cost **per agentic workflow** will rise more than fivefold through 2028 🔮
- Accenture CIO survey: 9 in 10 executives say cheaper tokens lead to more use cases; 1 in 20 would bank a 25% price cut 🟡
- Counter-trend: new top tiers priced higher (gpt-6-astra, Claude Fable 5.1: $10 / $50 per 1M) ✅
- Move the conversation from price per token to **cost per successful task**

**Speaker notes:**
The first surprise is that tokens really are getting cheaper, and the bill still goes up.

Epoch AI measured the price of reaching a fixed benchmark level: it falls about 47 percent per quarter, roughly 13 times per year since 2023, and across tasks anywhere from 9 to 900 times per year. That is verified on their publications, with their own caveats about benchmark gaming and about users not switching models as fast as the frontier moves.

At the same time, Gartner predicts that inference cost per agentic workflow will rise more than fivefold through 2028. That is a forecast, not a measurement. Accenture's CIO survey says nine in ten executives would spend price cuts on new use cases, and only one in twenty would bank a 25 percent price cut as savings. That is a survey by a consultancy, so treat it as a claim.

Both trends can be true at once: the unit price goes down while consumption per task goes up faster, because agents re-send context on every step, call sub-agents, retry and reason. And the newest top tiers are priced higher, not lower: 10 dollars in and 50 out per million tokens.

So price per token is the wrong headline. The number that matters is cost per successful task.

**Sources:** [Epoch AI: The plunging price of thought](https://epoch.ai/publications/the-plunging-price-of-thought), [Epoch AI: LLM inference price trends](https://epoch.ai/data-insights/llm-inference-price-trends), [Gartner press release 2026-08-17](https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028), [Accenture: CIO's guide to AI tokenomics](https://www.accenture.com/en/insights/ai-data/cios-guide-ai-tokenomics), [OpenAI pricing](https://platform.openai.com/docs/pricing), [research.md §1, §8](research.md)

## Slide 4 — Why the bill grows faster than usage looks
**Timing:** 1:30 (3:45–5:15)
**On slide:**
- **Statelessness**: every agent step re-sends instructions, tool definitions, history, tool results → cost grows with steps × context, not with user messages ✅
- **Output is the expensive side**: output costs 5× input on flagship cards (gpt-6.1-sol, Claude Sonnet 5.5: $2 / $10 per 1M) ✅
- **Reasoning tokens are billed as output** ("Output price (including thinking tokens)", Gemini) ✅
- **The billed prompt is not the typed prompt**: tokens are the meter (FinOps Foundation) ✅
- In our baseline: 403 output tokens were ~1/3 of the cost of a 4,231-token prompt 🧪

**Speaker notes:**
Why does the bill grow faster than usage seems to? Four mechanisms.

First, models are stateless. Every step of an agent re-sends the instructions, the tool definitions, the history and every tool result so far. So cost grows with the number of steps times the context size, not with the number of user messages. The OpenAI caching guide describes exactly this growing-prefix pattern.

Second, output is the expensive side. On the current flagship price cards output costs five times input: 2 dollars in, 10 dollars out per million tokens for both gpt-6.1-sol and Claude Sonnet 5.5.

Third, reasoning or thinking tokens are billed as output. Gemini's price page literally says "output price, including thinking tokens". You pay for text you never see.

Fourth, as the FinOps Foundation puts it, tokens are the meter, and the prompt the user typed is not the prompt that is billed.

In our baseline, the verbose answer was 403 output tokens against a 4,231-token prompt. Because of the 5x multiplier, those 403 tokens were about a third of the cost.

**Sources:** [OpenAI prompt caching guide](https://platform.openai.com/docs/guides/prompt-caching), [OpenAI pricing](https://platform.openai.com/docs/pricing), [Anthropic prompt caching / pricing](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), [FinOps for AI overview](https://www.finops.org/wg/finops-for-ai-overview/), [workshop-plan.md](workshop-plan.md) (Block 1), [research.md §1.2](research.md)

## Slide 5 — Price cliffs and multipliers
**Timing:** 1:30 (5:15–6:45)
**On slide:**
- Table, all ✅ as read on 2026-10-19:
  - Long context: OpenAI >272K-token requests 2× input; Claude Haiku 5.5 5× above 100K-token prompts
  - Data residency: +10% (OpenAI regional endpoints; Anthropic `inference_geo: "us"` 1.1×)
  - Speed tiers: OpenAI Fast 2×, Ultrafast 6× (gpt-6.1-sol); Gemini Priority 1.8×
  - Discount tiers: Batch / Flex −50% (OpenAI, Gemini), Batch −50% (Anthropic)
  - Promos end: Gemini 4 Argon $2/$10 until 30 Nov 2026, then $4/$20
- Free models cost $0 → nobody sees the bill; gateways treat $0 as "not budgeted" (LiteLLM docs) ✅
- Our workshop: every free call is shadow-priced at its paid twin's list price

**Speaker notes:**
The second set of surprises are multipliers that are easy to miss in a business case. All of these are from the provider pricing pages as read on October 19.

Long context: OpenAI charges double for input on requests over 272 thousand tokens; Claude Haiku 5.5 costs five times more above 100 thousand tokens. Data residency adds about 10 percent at both OpenAI and Anthropic. Speed tiers: OpenAI's Fast tier is twice the standard price, Ultrafast six times; Gemini Priority is 1.8 times. In the other direction, Batch and Flex tiers are half price for asynchronous work.

And promotions end. Gemini 4 Argon is 2 and 10 dollars per million until November 30, and doubles to 4 and 20 on December 1. A forecast built on the promo price doubles overnight. The FinOps Foundation explicitly warns about cost increases after preview and free phases.

The last trap is free models. A free tier costs zero, so nobody sees the bill until the migration to a paid endpoint. Gateways treat zero as "not budgeted": LiteLLM documents setting the cost to zero as the way to let free or on-prem models bypass budget checks. That is why in our workshop every free call is priced at its paid twin's list price. We call that a shadow cost.

**Sources:** [OpenAI pricing](https://platform.openai.com/docs/pricing), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), [Anthropic batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [LiteLLM custom pricing](https://docs.litellm.ai/docs/proxy/custom_pricing), [FinOps for AI overview](https://www.finops.org/wg/finops-for-ai-overview/), [comparison.md §4](comparison.md), [research.md §1.2](research.md)

## Slide 6 — Numbers not to quote without context
**Timing:** 1:15 (6:45–8:00)
**On slide:**
- McKinsey expert interview (14 Oct 2026): pilot → production "can nearly quadruple" cost; a poorly designed agent "up to 30 times as many tokens"; "a single user could rack up thousands of dollars in a single day" 🟡 no dataset
- Accenture: ~$2.5B spent on tokens last year by surveyed firms, consumption +78% in 24 months, 5-10× growth in six months (anecdotes) 🟡
- EY: seven cost categories of an agent; most business cases include only three (tokens, licences, infrastructure) 🟡
- Services market: EPAM Q2 2026 earnings call lists "token cost engineering" among AI-native engineering offerings; some spend shifting to "tokens, hardware and infrastructure" 🟡
- FrugalGPT "up to 98%" is one dataset (HEADLINES); others 59-73% ✅

**Speaker notes:**
Before we go further, a slide of numbers you will see in decks, and that should never be quoted without their context.

McKinsey published an expert interview a few days ago: moving a tool from pilot to production can nearly quadruple its cost, a poorly designed agent can use up to 30 times as many tokens, and by spring 2026 executives saw single users rack up thousands of dollars in a day. These are interview quotes. There is no published dataset behind them.

Accenture's tokenomics survey has big numbers: about 2.5 billion dollars spent on tokens by the surveyed enterprises, consumption expected to grow 78 percent in two years, anecdotes of five- to tenfold growth in six months. Self-reported. EY's useful point is qualitative: an agent has seven cost categories, and most business cases only include the first three. Orchestration, observability, governance and human review show up later.

From the services market, EPAM's public Q2 2026 earnings call lists token cost engineering among its AI-native engineering offerings and says some spend is shifting to tokens, hardware and infrastructure. That is a company describing its own business, so it is a vendor claim, but it is a signal that this is now a paid discipline.

And from research: FrugalGPT's "up to 98 percent" saving is on one dataset; on the others it was 59 to 73 percent.

**Sources:** [McKinsey: What does AI really cost?](https://www.mckinsey.com/featured-insights/mckinsey-explainers/what-does-ai-really-cost), [Accenture tokenomics](https://www.accenture.com/en/insights/ai-data/cios-guide-ai-tokenomics), [EY: agentic AI token costs](https://www.ey.com/en_us/insights/ai/agentic-ai-token-costs), [EPAM Q2 2026 call transcript (Motley Fool)](https://www.fool.com/earnings/call-transcripts/2026/08/06/epam-epam-q2-2026-earnings-call-transcript/), [FrugalGPT arXiv 2305.05176](https://arxiv.org/abs/2305.05176), [research.md §1.1, §4.1](research.md)

## Slide 7 — FinOps for AI: the community playbook
**Timing:** 1:45 (8:00–9:45)
**On slide:**
- State of FinOps 2026 (1,192 respondents, >$83B cloud spend): **98%** manage AI spend (31% two years earlier); FinOps for AI is the top forward-looking priority; many are asked to **self-fund AI through efficiency** ✅
- FinOps Foundation: "Basic Price × Quantity = Cost equation still applies" ✅
- Practices: showback before chargeback, tagging per use case, quotas, throttling, anomaly detection, caching, batching, commitments for predictable load ✅
- Crawl / walk / run: manual estimates + fail-fast limits → basic automation → automated tracking + ROI metrics ✅
- KPIs: cost per inference / token / API call, utilization, anomaly rate, ROI, **model choice quality score** ✅
- Still open: "lack of generally accepted frameworks for cost allocation across multi-agent workloads" ✅

**Speaker notes:**
What does the FinOps community actually recommend? First, this is now mainstream. In the State of FinOps 2026 survey, 98 percent of almost 1,200 respondents manage AI spend, up from 31 percent two years earlier. FinOps for AI is the top forward-looking priority, and many organizations are asked to fund AI out of efficiency gains elsewhere.

The FinOps Foundation's working-group guidance is refreshingly pragmatic. Price times quantity still applies: you either reduce the rate, with commitments and tiers, or the quantity, which is tokens. The practices are the familiar ones: showback before chargeback, tag and allocate per use case, set quotas and throttling, detect anomalies, then optimize with caching, batching and commitments where the load is predictable.

They describe a crawl, walk, run progression: in a pilot, manual estimates and fail-fast limits; once integrated, basic automation and anomaly analysis; in production, automated tracking and ROI-level metrics.

The KPI I like most is the "model choice quality score": is the model more capable, and more expensive, than the task needs? And the Foundation is honest about what is not solved: there is no generally accepted framework for allocating cost across multi-agent workloads.

**Sources:** [State of FinOps 2026 press release](https://www.linuxfoundation.org/press/state-of-finops-survey-ai-value-and-skills-top-priorities-as-finops-matures-across-technology-value-98-manage-ai-90-saas-64-licensing-48-data-center-1), [FinOps for AI overview](https://www.finops.org/wg/finops-for-ai-overview/), [How to build a GenAI cost and usage tracker](https://www.finops.org/wg/how-to-build-a-generative-ai-cost-and-usage-tracker/), [research.md §2.1](research.md)

## Slide 8 — FOCUS: billing data gets an AI shape
**Timing:** 1:30 (9:45–11:15)
**On slide:**
- FOCUS 1.4 (June 2026): open billing schema all major clouds emit; Invoice Detail + Billing Period datasets; no breaking changes ✅
- Already carries tokens: ConsumedQuantity / ConsumedUnit, SkuId, ServiceCategory "AI and Machine Learning" ✅
- FOCUS 1.5 (working draft, ratification planned **3 Dec 2026**) adds ✅:
  - `ModelDeveloper`, `ModelFamily`, `ModelId`, `ModelVersion`
  - `TokenDirection` (Input / Output; reasoning = Output), `TokenCacheAction` (Uncached / Read / Write / Other)
  - `PrincipalId`, `CredentialId`, `RequesterDetails`: who made the call, never the key itself
- Not in 1.5: reasoning tokens billed but not returned, cache storage fees, priority/batch tiers, provisioned throughput, agentic subcategories ✅
- Until providers emit 1.5: attribution comes from **your gateway logs** (our `to_focus.py`, not validated 🧪)

**Speaker notes:**
Finance needs the data in a shape it can join with everything else, and that shape is FOCUS, the FinOps Open Cost and Usage Specification. Version 1.4 was published in June 2026, and all major clouds emit FOCUS data natively. It already carries tokens as consumed quantity and unit, with an AI and Machine Learning service category. But practitioners still lack worked examples; one comment on the spec tracker says they work with over 20 AI vendors and every one has a different data format.

FOCUS 1.5 is a working draft with ratification planned for December 3, and it adds exactly what AI chargeback needs. Model identity: developer, family, id, version. Token direction, input or output, with reasoning counted as output. Token cache action: uncached, read, write. And new columns for who made the call: principal id and credential id, which developer, service or agent called the model, never the key string itself. Note what they do not say: who benefits, when a gateway calls on behalf of many users.

Also not in 1.5: reasoning tokens that are billed but not returned, cache storage fees, priority and batch tiers, provisioned throughput.

So today, attribution by team, feature or agent comes from your own gateway logs. In the workshop we shaped those logs like FOCUS with the 1.5 draft property names. We did not run the FOCUS validator on it.

**Sources:** [FOCUS 1.4 changelog](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/blob/v1.4/CHANGELOG.md), [Introducing FOCUS 1.4](https://www.finops.org/insights/introducing-focus-1-4/), [FOCUS for AI](https://focus.finops.org/technology-categories/focus-for-ai/), [FOCUS FR #1941](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/issues/1941), [FOCUS 1.5 release scope](https://focus.finops.org/focus-1-5-release-scope/), [workshop/ex4_gateway/to_focus.py](workshop/ex4_gateway/to_focus.py), [research.md §2.2](research.md)

## Slide 9 — The unit metric: $ per successful task
**Timing:** 1:45 (11:15–13:00)
**On slide:**
- Three numbers per feature 🧪:
  - **$ per task** (a ticket, a document, a conversation)
  - **$ per successful task** = $/task ÷ pass rate → a cheap but wrong config is penalized
  - **$ per month at forecast volume**
- FinOps Foundation: cost per inference / call / token, tied to value ✅; McKinsey interviewee: "It's not just about cost per token. It's about cost per task." 🟡
- Shadow-price free and internal models; **state the price card and its date**
- Same configs, two price cards 🧪: B (large) vs E (small) differ **~9×** on paid-twin prices ($0.60/$2.40 vs $0.07/$0.20) and **~20×** on the frontier card (gpt-6.1-sol $2/$10 vs gpt-6-luna $0.10/$0.50)

**Speaker notes:**
So what do we measure? We recommend three numbers per feature, and the workshop computes all three.

Cost per task, where the task is the business unit: a ticket, a document, a conversation. Cost per successful task, which is cost per task divided by the pass rate on your eval set. That penalizes a configuration that is cheap but wrong: configuration G from the first slide costs 19 thousandths of a cent per ticket on paper, but almost twice that per successful ticket. And cost per month at forecast volume, because that is the number someone will sign.

This matches the FinOps Foundation's KPIs, and one of McKinsey's interviewees said it in one sentence: it's not about cost per token, it's about cost per task.

Two practical rules. Shadow-price everything that looks free: free tiers, internal models, credits. And always state the price card and its date. Here is why: the same two configurations, a large and a small model with the same prompt, are about 9 times apart if you price them at the paid twins of the free models we used, and about 20 times apart on a frontier price card. Same tokens, same quality, different business case. Whoever chooses the price card chooses the conclusion.

**Sources:** [FinOps for AI overview](https://www.finops.org/wg/finops-for-ai-overview/), [McKinsey](https://www.mckinsey.com/featured-insights/mckinsey-explainers/what-does-ai-really-cost), [workshop-plan.md](workshop-plan.md) (Block 1, twin vs frontier), [workshop/results/prices_snapshot.json](workshop/results/prices_snapshot.json), [research.md §3](research.md)

## Slide 10 — The test subject: a ticket-reply pipeline
**Timing:** 1:00 (13:00–14:00)
**On slide:**
- Fictional invoicing SaaS "Ledgerly": 16 tickets, a knowledge base of sections (~4.2k tokens), JSON reply {category, reply, sources, confidence}
- Automatic checks per ticket: valid JSON, right category, required facts present (regex) → pass/fail
- Levers as switches: model (large/small), context (full KB / BM25 top-3), prefix (dynamic header / stable), style (verbose / concise + max_tokens), cascade (+ grounding check)
- Free OpenRouter models: Nemotron 3 Ultra 550B (large) and Nemotron 3.5 Lightning (small); reasoning, retries, fallbacks off 🧪
- Shadow prices: paid twin and frontier card; **n=16, one run per config** 🧪

**Speaker notes:**
A minute on the test subject, so you know what the numbers mean. The pipeline answers support tickets for a fictional invoicing SaaS called Ledgerly. There are 16 tickets and a knowledge base of about 4,200 tokens. The model returns JSON: a category, the reply, the knowledge-base sections it used and a self-reported confidence.

Each answer is checked automatically: is the JSON valid, is the category right, and does the reply contain the required facts, checked with regular expressions. That gives pass or fail per ticket.

Every lever is a switch in the code: large or small model, the whole knowledge base or the BM25 top three sections, a dynamic header at the top of the prompt or a stable prefix, verbose or concise output with a token cap, and a cascade with or without a grounding check.

The models are two free Nemotron models on OpenRouter, with reasoning, retries and provider fallbacks switched off, and every call is shadow-priced. And again: 16 tickets, one run per configuration.

**Sources:** [workshop/app/pipeline.py](workshop/app/pipeline.py), [workshop/app/checks.py](workshop/app/checks.py), [workshop/app/tickets.jsonl](workshop/app/tickets.jsonl), [workshop-plan.md](workshop-plan.md)

## Slide 11 — Lever lab: cost vs quality
**Timing:** 2:00 (14:00–16:00)
**On slide:**
- Bar chart: $/month at 100k tickets (frontier card) with pass rate per config 🧪
  - A baseline $1,250 · 14/16
  - B concise $928 · 15/16 (−26%)
  - C stable prefix $931 · 14/16
  - D trimmed context $394 · 15/16 (−68%)
  - E / F small model $46 · 14/16 (−96%)
  - G small + trimmed $19 · **9/16** (−98%)
  - H cascade (confidence check) $65 · 13/16
  - I cascade + grounding $65 · 14/16 (−95%)
- Concise output also cut p50 latency 8.9 s → 2.3 s 🧪

**Speaker notes:**
Here is the whole lever lab on one chart. Bars are dollars per month at 100,000 tickets on the frontier price card; the label is the pass rate.

Concise output, B, saved 26 percent: output fell from 403 to 85 tokens, and quality went from 14 to 15 of 16. It also cut median latency from almost 9 seconds to 2.3. Cheaper, faster and not worse is a rare combination; take it first.

C moved the dynamic header out of the system prompt. On its own it does not change price here, because the free endpoint did not cache in this run; it is the precondition for caching, which I will show later.

D trimmed the context to the top three retrieved sections: minus 68 percent, 15 of 16. On this model, trimming was the biggest lever.

The small model, E and F, is minus 96 percent at 14 of 16. G, small plus trimming, is the 98 percent saving with 9 of 16. And the two cascades, H and I, answer with the small model and escalate to the large one; they land at about minus 95 percent, and the difference between them is the topic of the next slides.

Read the quality column with care: 15 versus 14 of 16 is one ticket. It does not mean concise output improves quality; it means it did not visibly hurt it.

**Sources:** [workshop-plan.md](workshop-plan.md) (Block 1 table), [workshop/results/levers_summary_A-H.md](workshop/results/levers_summary_A-H.md), [workshop/results/levers_summary_I.md](workshop/results/levers_summary_I.md), [workshop/ex2_levers/run_levers.py](workshop/ex2_levers/run_levers.py)

## Slide 12 — Levers: research size vs our measurement
**Timing:** 1:45 (16:00–17:45)
**On slide:**
- Table: lever · published size · main risk · ours
  - Output caps: ∝ output share (5× input price) ✅ · truncation · −26% 🧪
  - Context trimming / RAG: ∝ input share · retrieval misses · −68%, BM25 recall@3 14/16 🧪
  - Routing / cascade: RouteLLM >2× (3.66× MT-Bench, 1.4-1.5× MMLU/GSM8K) ✅; FrugalGPT up to 98% on one dataset ✅ · hallucinations, weak escalation signal · −95% 🧪
  - Prompt caching: reads 0.05-0.10×, writes 1.0-2.0× ✅ · dynamic prefix, TTL · 0 vs 6,288 cached tokens 🧪
  - Semantic cache: vCache: thresholds cannot separate correct/incorrect hits ✅ · wrong answers · 9/12 near-misses wrong 🧪
  - Batch / Flex: −50%, async ✅ · latency · not run
  - Prompt compression: LLMLingua up to 20× with 1.5-pt drop ✅ · task loss, breaks caching · not run
  - Distillation: 770M T5 beat 540B PaLM on two benchmarks ✅ · training + eval cost · not run

**Speaker notes:**
This is the reference table: for each lever, the size the literature or the provider reports, the main risk, and what we measured.

Output caps and context trimming are proportional to the share of output or input in your bill. Their risks are truncation and retrieval misses; our retrieval found the right sections for 14 of 16 tickets, and the large model compensated on the misses.

Routing and cascades: RouteLLM reports more than 2x savings at near-GPT-4 quality, but it is benchmark-dependent, 3.66x on MT-Bench and only 1.4 to 1.5x on MMLU and GSM8K. FrugalGPT is up to 98 percent on one dataset. The risk is that the small model hallucinates and your escalation signal does not notice.

Prompt caching: reads cost 5 to 10 percent of normal input, writes cost 1 to 2 times, depending on provider. Semantic caching: the vCache paper shows that similarity thresholds cannot separate correct from incorrect hits.

Batch and Flex tiers are a flat 50 percent for asynchronous work. Prompt compression and distillation have impressive paper numbers, LLMLingua up to 20x, a 770-million-parameter T5 beating 540-billion PaLM on two benchmarks, but we did not run batch, compression or distillation. Note that compression competes with caching: a prompt that changes on every request cannot be cached.

**Sources:** [RouteLLM arXiv 2406.18665](https://arxiv.org/abs/2406.18665), [FrugalGPT arXiv 2305.05176](https://arxiv.org/abs/2305.05176), [vCache arXiv 2502.03771](https://arxiv.org/abs/2502.03771), [LLMLingua arXiv 2310.05736](https://arxiv.org/abs/2310.05736), [Distilling step-by-step arXiv 2305.02301](https://arxiv.org/abs/2305.02301), [OpenAI batch](https://platform.openai.com/docs/guides/batch), [research.md §4](research.md), [comparison.md §5](comparison.md)

## Slide 13 — Levers interact, and n=16 is small
**Timing:** 1:15 (17:45–19:00)
**On slide:**
- Small model on full KB: 14/16 · trimmed context on large model: 15/16 · **both together: 9/16** (mostly wrong categories) 🧪
- Two "safe" levers stacked can break quality → **re-run the eval set after every lever**
- Our checks have blind spots too: F "passed" T11 with an invented "$5,000 per year" because it also said "contact sales for a custom quote" 🧪
- Statistics: 16 tickets, one run per config, one model pair → **1-2 ticket differences are noise**; 14/16 vs 15/16 is not a quality gain
- Robust: token counts and cost deltas (−26%, −68%, −96%); the 9/16 collapse (5 tickets) is a signal worth re-testing, not a law

**Speaker notes:**
Two warnings before we go deeper.

First, levers interact. The small model on the full knowledge base passed 14 of 16. Context trimming on the large model passed 15 of 16. Both together passed only 9, mostly with wrong categories. Our reading: the small model needed the full context that the large model could do without. Stacking two levers that are each safe can break quality, which is why every lever change needs the eval set re-run.

Second, our own checks have blind spots. Configuration F was counted as a pass on ticket 11 although it invented a base price of 5,000 dollars a year, because it also said "contact sales for a custom quote", and that satisfied the regex. The quality numbers are only as good as the checks.

And the statistics. This is 16 tickets, one run per configuration, one model pair. A difference of one or two tickets is noise. 14 versus 15 is not a quality improvement, and 13 versus 14 is not a regression. What is robust are the token counts and the cost deltas, because they do not flip from run to run. The drop to 9 of 16 is five tickets, big enough to take seriously and re-test, but not a law about small models.

**Sources:** [workshop-plan.md](workshop-plan.md) (Block 1 discussion points), [workshop/results/levers_A-H_2026-10-19.json](workshop/results/levers_A-H_2026-10-19.json), [workshop/app/checks.py](workshop/app/checks.py), [research.md §10](research.md)

## Slide 14 — A cascade is only as good as its verifier
**Timing:** 1:30 (19:00–20:30)
**On slide:**
- Diagram: ticket → small model → verifier → reply; verifier fails → large model (trimmed context) → reply
- Verifier H (no LLM call): valid JSON, known category, known sources, self-reported confidence ≥ 0.75 🧪
- Verifier I: H + **every number in the reply must exist in the KB or the ticket** (`$` kept: KB has "5,000 files", never "$5,000") 🧪
- H: escalated 1/16 (invalid JSON); confidence was ≥ 0.75 on 15/16 small-model answers, including wrong ones → 13/16 🧪
- I: grounding check escalated T11 → 14/16 at −95% 🧪
- Research routers (RouteLLM, FrugalGPT) learn the escalation signal ✅; ours is ~10 lines of deterministic code 🧪

**Speaker notes:**
Here is the cascade. A ticket goes to the small model first. A cheap verifier, with no extra LLM call, decides whether to accept the answer. If it rejects, the ticket goes to the large model on trimmed context.

Verifier H checks the format: valid JSON, a known category, known source sections, and the model's own confidence at least 0.75. It escalated exactly one ticket of 16, for invalid JSON. The small model reported high confidence on 15 of 16 answers, including the wrong ones. Self-reported confidence is not an escalation signal.

Verifier I adds one deterministic rule: every number in the reply, prices, limits, days, must appear in the knowledge base or in the ticket. It is about ten lines of code. One detail mattered: the comparison keeps the dollar sign. In an earlier run the small model invented "5,000 dollars", and a naive check let it through because "5,000" appears in the knowledge base as a file count.

With the grounding check the cascade escalated ticket 11, the large model answered it correctly, and we got 14 of 16 at minus 95 percent. The research routers learn their escalation signal from data; the lesson here is that the escalation signal is the product.

**Sources:** [workshop/app/pipeline.py](workshop/app/pipeline.py) (`validate`, `ungrounded_numbers`), [workshop/results/levers_summary_I.md](workshop/results/levers_summary_I.md), [workshop-plan.md](workshop-plan.md), [RouteLLM](https://arxiv.org/abs/2406.18665), [FrugalGPT](https://arxiv.org/abs/2305.05176), [research.md §4.1](research.md)

## Slide 15 — T11: the invented Enterprise price
**Timing:** 1:30 (20:30–22:00)
**On slide:**
- Ticket T11: "We have about 120 people in finance and need Okta SSO. What plan do we need and what does it cost?"
- Small model (H run): "Enterprise plan is required for Okta SSO. Minimum 50 seats, annual contract only. Base price **$9,900/year** …" · confidence **0.95** · H verifier: ok → served · facts check: fail 🧪
- I run: verifier → "ungrounded numbers ['$9900']" → escalated 🧪
- Large model: "… Enterprise has **custom pricing**, a minimum of 50 seats, and requires an annual contract. For 120 seats, contact sales for a quote." → pass 🧪
- Cost of escalating T11: 2 calls instead of 1, still −95% overall 🧪

**Speaker notes:**
This is ticket 11 side by side. The customer has 120 people in finance, needs Okta SSO, and asks what plan they need and what it costs.

The knowledge base says Enterprise has custom pricing. The small model answered: Enterprise, minimum 50 seats, annual contract, base price 9,900 dollars a year. That price does not exist anywhere. It reported confidence 0.95. Verifier H looked at format and confidence and said OK, so in production this goes to the customer: a sales commitment nobody made.

In the I run, the grounding check found a dollar amount that does not appear in the knowledge base and escalated. The large model said Enterprise has custom pricing, minimum 50 seats, contact sales for a quote. Correct.

Escalation means two calls for this ticket instead of one, and the whole configuration is still about 95 percent cheaper than the baseline. The cheap check costs nothing per request and is the difference between a cost saving and a liability.

**Sources:** [workshop/app/tickets.jsonl](workshop/app/tickets.jsonl) (T11), [workshop/results/levers_A-H_2026-10-19.json](workshop/results/levers_A-H_2026-10-19.json) (H_cascade T11), [workshop/results/levers_I_2026-10-19.json](workshop/results/levers_I_2026-10-19.json) (I_cascade_grounded T11), [workshop-plan.md](workshop-plan.md)

## Slide 16 — Prompt caching: keep the prefix stable
**Timing:** 1:45 (22:00–23:45)
**On slide:**
- Diagram: dynamic prefix [time · ticket id · session uuid][instructions][KB] → every request a new prefix; stable prefix [instructions][KB] + user turn [time · id][ticket] → shared prefix
- Provider rules ✅: OpenAI GPT-5.6+ write 1.25×, read 0.10× (0.05× gpt-6.1-sol), min 1,024 tokens; Anthropic write 1.25× (5 min) / 2× (1 h), read 0.10× (0.05× Opus/Sonnet 5.5); Gemini implicit, no write fee
- Measured, ~8.1k-token prompt, 4 sequential requests: dynamic **0** cached tokens; stable **6,288 cached tokens** from the 2nd request on (twin cost −24% over the probe) 🧪
- On ~4.2k prompts both got 0 in one probe, 15% in a later run: free-endpoint caching is undocumented ❌ → qualitative only
- Rules from the docs ✅: stable first, dynamic last; append, don't rewrite history; keep tools and their order stable; compaction resets the prefix; per-customer `prompt_cache_key` also prevents cache-hit probing

**Speaker notes:**
Prompt caching is the biggest "free" lever, with one condition: the prefix must be byte-identical.

A very common pattern puts the current time, a request id or a session id at the top of the system prompt. Then every request has a new prefix, and nothing is ever reused. The fix is to keep instructions and knowledge first and move everything dynamic to the end, into the user turn.

The providers now converge: OpenAI on GPT-5.6 and later charges 1.25 times for a cache write and a tenth for a read, a twentieth on gpt-6.1-sol, with a minimum of 1,024 tokens. Anthropic is 1.25 times for a 5-minute write, 2 times for one hour, reads a tenth or less. Gemini caches implicitly with no write fee.

We probed it on the free endpoint with an 8,100-token prompt and four sequential requests. Dynamic header: zero cached tokens. Stable prefix: 6,288 cached tokens on every request from the second one on, which cut the shadow cost of the probe by 24 percent. On the shorter 4,200-token prompt the free endpoint cached nothing in one probe and 15 percent in a later run. Its caching is undocumented, so treat our numbers as qualitative.

The provider docs give the rules: stable first, dynamic last, append history instead of rewriting it, keep tool definitions and their order stable, and remember that compaction resets the prefix. There is also a privacy angle: OpenAI recommends a per-customer cache key partly to prevent cache-hit probing across users.

**Sources:** [OpenAI prompt caching](https://platform.openai.com/docs/guides/prompt-caching), [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Gemini caching](https://ai.google.dev/gemini-api/docs/caching), [OpenRouter prompt caching](https://openrouter.ai/docs/guides/best-practices/prompt-caching), [workshop/results/cacheprobe-20261019-165014.json](workshop/results/cacheprobe-20261019-165014.json), [workshop/ex2_levers/cache_probe.py](workshop/ex2_levers/cache_probe.py), [workshop-plan.md](workshop-plan.md) (Block 2), [research.md §4.2](research.md)

## Slide 17 — When caching costs more than no caching
**Timing:** 1:15 (23:45–25:00)
**On slide:**
- Simulation on our measured prompt shape (stable prefix ~4,173 + ~45 tokens/ticket), input-cost multiplier vs no caching, by requests sharing the prefix within one TTL window 🧪 (provider rules ✅):
  - OpenAI GPT-5.6+ / Anthropic 5-min: N=1 **1.25×** · N=2 0.68× · N=5 0.34× · N=20 0.17× · N=100 0.12×
  - OpenAI gpt-6.1-sol: 1.25× · 0.65× · 0.30× · 0.12× · 0.07×
  - Anthropic 1-hour: **1.99×** · 1.05× · 0.49× · 0.20× · 0.13×
  - Gemini implicit: 1.00× · 0.53× · 0.25× · 0.11× · 0.07×
- A dynamic value at the top makes every request N=1: you pay the write premium and never read
- Watch also: OpenAI "minimum cacheable length cost trap"; cached tokens still count toward rate limits ✅

**Speaker notes:**
Caching is not automatically a saving. This table is a simulation: our measured prompt shape, the published provider multipliers, and the number of requests that share the prefix within one cache lifetime.

With a write premium, a cache that is written once and never read costs more than no caching: 1.25 times on OpenAI and Anthropic's 5-minute cache, almost 2 times with Anthropic's one-hour cache. With two requests per window you roughly break even or save a third. With 5 requests you pay about a third, with 100 requests about a tenth of the input cost.

And that is the point of the previous slide: a dynamic value at the top of the prompt makes every request N equals 1. You pay the write premium on every call and never read anything back.

Two more traps from the OpenAI docs: there is a documented cost trap for prefixes just under the minimum cacheable length, and cached tokens still count toward your rate limits. Measure the cache hit rate by model; FOCUS 1.5 includes exactly that as an example query.

**Sources:** [workshop/results/caching_sim_C_stable.md](workshop/results/caching_sim_C_stable.md), [workshop/ex2_levers/caching_sim.py](workshop/ex2_levers/caching_sim.py), [OpenAI prompt caching](https://platform.openai.com/docs/guides/prompt-caching), [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [FOCUS 1.5 scope](https://focus.finops.org/focus-1-5-release-scope/), [workshop-plan.md](workshop-plan.md) (Block 2)

## Slide 18 — Semantic cache: cheap wrong answers
**Timing:** 1:30 (25:00–26:30)
**On slide:**
- Chart: threshold sweep, bge-small-en-v1.5, 24 hand-built pairs (12 paraphrases, 12 near-misses with a different correct answer) 🧪
  - 0.80: **8/12** paraphrases saved, **9/12** near-misses served the **wrong** answer
  - 0.85: 3/12 vs 6/12 · 0.95: 0/12 vs 0/12
- Mean similarity: near-misses **0.836** > paraphrases 0.824 🧪
- Worst: "SAML SSO on the Business plan?" vs "… Enterprise plan?" = **0.946**; "export" vs "import invoices" = 0.932 🧪
- vCache (ICLR 2026): correct vs incorrect hits overlap (0.85 vs 0.84); optimal threshold varies 0.71-1.0 per item ✅
- Pairs are adversarial by design: a stress test, not a traffic estimate. Exact-match cache: 0 false hits 🧪

**Speaker notes:**
Semantic caching sounds like the ultimate lever: if a new question means the same as an old one, return the old answer for free. The problem is that "means the same" is decided by an embedding similarity threshold.

We built 24 pairs: 12 true paraphrases and 12 near-misses that look alike but have a different correct answer. With a common small embedding model, the near-misses scored higher on average than the paraphrases. At a threshold of 0.80, a semantic cache would save 8 of 12 paraphrase calls, and serve the wrong cached answer to 9 of 12 near-misses. "Is SAML SSO available on the Business plan" versus "on the Enterprise plan" scored 0.946. Export versus import invoices, 0.932.

This matches the vCache paper from ICLR 2026: on 45,000 samples the similarity distributions of correct and incorrect cache hits overlap, with means of 0.85 and 0.84, and the optimal threshold varies per cached item from 0.71 to 1.0, so no global threshold can guarantee correctness.

Fairness note: our pairs are deliberately adversarial, so this is a stress test, not a prediction for your traffic. The practical rule: take the safe win with exact-match caching, and use semantic caching only with per-domain validation, short lifetimes, and never for account-specific or numeric answers. A wrong answer at zero cost is not a saving.

**Sources:** [workshop/results/semantic_cache_embeddings.md](workshop/results/semantic_cache_embeddings.md), [workshop/results/semantic_cache_lexical.md](workshop/results/semantic_cache_lexical.md), [workshop/ex3_semantic_cache/pairs.jsonl](workshop/ex3_semantic_cache/pairs.jsonl), [vCache arXiv 2502.03771](https://arxiv.org/abs/2502.03771), [research.md §4.3](research.md)

## Slide 19 — One path to the models: the gateway
**Timing:** 1:30 (26:30–28:00)
**On slide:**
- Diagram: teams/features → virtual keys + per-request tags → **gateway** (allow-list, budget check, price table, rate limits) → providers; spend logs → FOCUS-shaped export → showback / chargeback
- AWS Bedrock guidance ✅: stamp attribution "in a shared client wrapper or LLM gateway"; restrict the call path (SCPs / IAM) so it is the only route; low-cardinality tags for billing, high-cardinality ids only in logs; no PII in tags; reconcile log-derived cost with the invoice
- Native options ✅: Bedrock application inference profiles + cost-allocation tags; Azure APIM `llm-token-limit` (429 per minute / 403 quota) + `llm-emit-token-metric`
- FinOps Foundation: the allocation problem is identifying the **consumer** of a shared model ✅

**Speaker notes:**
Now attribution and budgets. The FinOps Foundation names the core allocation problem for AI: identifying the consumer of a shared model. Their example: a tech support chatbot and a new-customer chatbot share the same model, and the invoice does not say which one spent what.

The clearest architecture statement I found is from AWS's Bedrock cost-attribution guidance, and it is not AWS-specific. Stamp attribution in a shared client wrapper or an LLM gateway. Restrict the call path, with policies and IAM, so the gateway is the only route to the models. Use low-cardinality tags, team, feature, environment, for billing, and keep high-cardinality ids like user or request only in the logs. Never put personal data in tags. And reconcile the cost you compute from logs against the actual invoice.

The diagram is that flow: each team gets a key, each request carries tags, the gateway enforces a model allow-list, checks the budget, prices the call from its price table, and writes spend logs that you export in a FOCUS shape for showback and later chargeback.

The clouds have native pieces: Bedrock application inference profiles with cost-allocation tags, Azure API Management's token-limit policy, which returns 429 for per-minute limits and 403 when a quota is used up, plus a metric policy for chargeback dashboards.

**Sources:** [AWS Bedrock cost attribution best practices](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-best-practices.html), [Bedrock application inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-application-inference-profiles.html), [Azure APIM llm-token-limit](https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy), [FinOps for AI overview](https://www.finops.org/wg/finops-for-ai-overview/), [research.md §5](research.md)

## Slide 20 — What the gateway actually did
**Timing:** 1:30 (28:00–29:30)
**On slide:**
- LiteLLM v1.106.0 OSS + Postgres 16, frontier shadow prices in the model config 🧪
- Team **support** ($0.05 budget): requests 1-6 served, #7 → HTTP 422 "Budget has been exceeded"; final spend $0.05619 = **112%** (check runs before the call) 🧪
- Team **growth** ($0.01, small model only): `large` → HTTP **403** (not on allow-list); 2 small calls $0.00091 🧪
- Gotchas 🧪: team spend lags one request; key-level tags = Enterprise-only (403), per-request `metadata.tags` work; with the `openrouter/` prefix our custom prices were logged as **$0** → budgets never tripped; root cause found 🧪: LiteLLM uses OpenRouter's own `usage.cost` (0 for `:free`) before custom prices
- Cloudflare documents the same: spend limits are eventually consistent, may overshoot ✅
- `to_focus.py`: one FOCUS-shaped row per model × token direction × cache action, `PrincipalId` = key alias, never the key 🧪

**Speaker notes:**
We ran this with LiteLLM, self-hosted, open-source version 1.106, with Postgres, and frontier shadow prices in its model config.

The support team had a budget of five cents and access to both models. Requests one to six were served, request seven was rejected with "Budget has been exceeded". But the final spend was 5.6 cents, 112 percent of the budget, because the check happens before the call using spend already recorded, so the request that crosses the line is still served. Size budgets with at least one request of headroom. Cloudflare documents the same eventual consistency for its spend limits.

The growth team was allowed only the small model. Its call to the large model got a 403. The allow-list is a cost control in itself.

Three gotchas. The team spend shown to the client application lags by one request. Tags on the key itself are an Enterprise feature in LiteLLM; tags on each request work. And the big one: when we routed free models with the openrouter provider prefix, the gateway logged every call at zero dollars despite our custom prices, so the budgets never tripped. Switching to the generic OpenAI-compatible provider fixed it. The root cause: LiteLLM's OpenRouter integration takes the cost that OpenRouter itself reports in each response, and for free models that is zero, and it uses that number before it ever looks at your custom prices. Verify your gateway's cost numbers against a hand calculation before you trust a budget built on them.

Finally, a small script turned the spend logs into FOCUS-shaped rows: one per model, token direction and cache action, with the key alias as principal id, never the key.

**Sources:** [workshop/results/gateway_run.md](workshop/results/gateway_run.md), [workshop/results/chargeback_gateway.md](workshop/results/chargeback_gateway.md), [workshop/results/focus_gateway.csv](workshop/results/focus_gateway.csv), [workshop/ex4_gateway/litellm_config.yaml](workshop/ex4_gateway/litellm_config.yaml), [LiteLLM budgets](https://docs.litellm.ai/docs/proxy/users), [Cloudflare AI Gateway spend limits](https://developers.cloudflare.com/ai-gateway/features/spend-limits/), [workshop-plan.md](workshop-plan.md) (Block 4)

## Slide 21 — Self-host or API: a utilization question
**Timing:** 1:30 (29:30–31:00)
**On slide:**
- Chart: self-host $ per 1M output tokens vs average utilization, against API lines $8.40 (open-weights via API, $0.60/$2.40) and $30 (frontier, $2/$10) 🧪 (arithmetic)
- Assumptions: 8×H100 at $3.50/GPU-h 🟠, always on, $15k/month ops, **assumed** 5,000 output tok/s per replica, 10 input tokens per output token → fixed $35,440/month 🧪
- Break-even: **64%** utilization vs open-weights API, **18%** vs frontier price 🧪
- At ~$10/GPU-h (hyperscaler-like list 🟠): open-weights comparison never breaks even (133%), frontier 37% 🧪
- Business-hours-only traffic (50 of 168 h/week) caps an always-on replica at **~30%** 🧪
- Published blog break-even: 72% sustained utilization for a 2×H100 server vs serverless 🟠

**Speaker notes:**
Should you self-host? The cost answer is a utilization question.

Our calculator makes every assumption explicit. One replica is 8 H100s at 3.50 dollars per GPU hour, a specialist-cloud price from a secondary price index, always on, plus 15,000 dollars a month of operations. That is about 35,000 dollars a month fixed. Throughput is assumed at 5,000 output tokens per second per replica; that is an assumption, not a benchmark.

The curve is self-hosted cost per million output tokens as utilization rises. It crosses the open-weights API price, 8.40 dollars per million output tokens including input, at 64 percent average utilization. It crosses a frontier API price at 18 percent, but that compares different models with different quality.

At hyperscaler-like GPU prices, around 10 dollars an hour, the open-weights comparison never breaks even; you would need 133 percent. And a simple arithmetic check: if traffic only comes in business hours, an always-on replica cannot average more than about 30 percent, even if it is saturated during the day.

Published break-evens vary by an order of magnitude; one blog puts it at 72 percent for a two-GPU server. Many self-hosting decisions are driven by residency, latency or model control rather than cost. Price those separately; don't hide them in the token math.

**Sources:** [workshop/results/breakeven_default.md](workshop/results/breakeven_default.md), [workshop/results/breakeven_hyperscaler.md](workshop/results/breakeven_hyperscaler.md), [workshop/ex5_breakeven/breakeven.py](workshop/ex5_breakeven/breakeven.py), [GPU Economy price index](https://gpueconomy.com/price-index), [GetDeploying H100](https://getdeploying.com/gpus/nvidia-h100), [break-even blog example](https://www.francisokafor.com/field-notes/self-hosted-open-weights-break-even-utilisation), [FinOps: choosing an AI approach](https://www.finops.org/wg/choosing-an-ai-approach-and-infrastructure-strategy/), [research.md §6](research.md)

## Slide 22 — Gateway landscape
**Timing:** 1:00 (31:00–32:00)
**On slide:**
- LiteLLM proxy: OSS (MIT); budgets per key/user/team, tag budgets, allow-lists; some features Enterprise ✅ · tested 🧪
- Portkey → Prisma AIRS AI Gateway (acquired by Palo Alto Networks, 2026): OSS gateway; Production $49/month; granular budgets on Enterprise ✅
- Cloudflare AI Gateway: core features free; spend limits by model/provider/metadata, eventually consistent; exact-match cache only ✅
- OpenRouter: no inference markup, 5.5% credit fee; key/workspace limits; cost in every response ✅ · used 🧪
- Azure APIM `llm-token-limit` · Kong AI Rate Limiting Advanced (tokens or **cost**) · Envoy AI Gateway (OSS, token limits) ✅
- Rule: pick what your platform team can operate, make it the **only** path, test its budgets and price table yourself

**Speaker notes:**
A quick map of gateways, all from vendor docs except LiteLLM, which we ran, and OpenRouter, which we used as the provider.

LiteLLM is open source under MIT, with budgets per key, user and team, tag budgets and allow-lists; some features are Enterprise-only. Portkey was acquired by Palo Alto Networks this year and is now Prisma AIRS AI Gateway; the gateway is open source, the platform has a 49-dollar production tier, and granular budgets are listed under Enterprise. Cloudflare's AI Gateway has its core features free, spend limits that are eventually consistent, and caches only identical requests. OpenRouter has no markup on inference, a 5.5 percent fee on credits, and returns the cost in every response. Azure API Management, Kong and Envoy give you token-based limits; Kong can limit by computed cost.

The decision rule is boring on purpose: start with the gateway your platform team can actually operate, make it the only path to model APIs, and test its budget enforcement and price table yourself before trusting its numbers.

**Sources:** [comparison.md §2](comparison.md), [LiteLLM enterprise](https://docs.litellm.ai/docs/enterprise), [Portkey pricing](https://portkey.ai/pricing), [Palo Alto Networks press release](https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-portkey-to-secure-ai-agents), [Cloudflare AI Gateway pricing](https://developers.cloudflare.com/ai-gateway/reference/pricing/), [OpenRouter pricing](https://openrouter.ai/pricing), [Kong AI Rate Limiting Advanced](https://developer.konghq.com/ai-gateway/policies/ai-rate-limiting-advanced/), [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)

## Slide 23 — What we did not verify
**Timing:** 1:00 (32:00–33:00)
**On slide:**
- Our workshop 🧪: one free model pair, **16 tickets, one run per config** → 1-2 ticket differences are noise; our regex checks missed an invented "$5,000"
- Provider caching on **paid** endpoints not measured; free-endpoint caching undocumented ❌; multipliers applied by simulation
- Gateways: only LiteLLM v1.106.0 OSS tested; Portkey, Cloudflare, Kong, Envoy, Azure APIM, Bedrock attribution = docs only; `$0` root cause traced in LiteLLM's source and reproduced once, not reported upstream 🧪
- Not run: batch APIs, prompt compression, distillation
- FOCUS export hand-shaped from 1.4 columns + 1.5 **draft** names; not validated
- Surveys and interviews (Accenture, McKinsey, EY) 🟡; Gartner 🔮; GPU prices and blog break-evens 🟠; our throughput is an assumption

**Speaker notes:**
Before the checklist, what we did not verify, so you can calibrate everything I said.

Our own numbers are small: one free model pair, 16 tickets, one run per configuration. Differences of one or two tickets are noise, and our regex checks counted at least one invented price as a pass.

We did not measure provider caching on paid endpoints. The free endpoint's caching is undocumented and sporadic, so the caching savings come from a simulation with published multipliers.

We only tested LiteLLM's open-source version. Everything about Portkey, Cloudflare, Kong, Envoy, Azure and Bedrock comes from documentation, and we traced the zero-dollar pricing bug in LiteLLM's source and reproduced it, but did not report it upstream. We did not run batch APIs, prompt compression or distillation. Our FOCUS export is shaped by hand from the 1.4 columns and the 1.5 draft names and was not validated.

The survey and interview numbers are self-reported by their publishers, the Gartner number is a forecast, the GPU prices and published break-evens are secondary, and our GPU throughput is an assumption.

**Sources:** [research.md §10](research.md) (open items), [workshop-plan.md](workshop-plan.md), [comparison.md](comparison.md)

## Slide 24 — AI cost-control checklist
**Timing:** 1:15 (33:00–34:15)
**On slide:**
- 1 Pick the unit; report **$/task and $/successful task** next to quality, plus $/month at forecast volume
- 2 Shadow-price free and internal models; **state the price card and its date**
- 3 One path to models: a gateway with team/feature attribution; test its budgets and price table
- 4 Budgets with one request of headroom, model allow-lists, anomaly alerts
- 5 Levers in order of risk: output caps → stable prefix / caching → context trimming → batch for async → small model or cascade with a **deterministic** verifier → semantic cache last, with validation
- 6 Re-run the eval set after every lever; levers interact
- 7 FOCUS-shaped export for finance; reconcile with the invoice

**Speaker notes:**
If you remember one slide, take this one.

Pick the unit, the ticket, the document, the conversation, and report cost per task and cost per successful task next to quality, plus the monthly number at forecast volume. Shadow-price everything that looks free, and always state the price card and its date.

Put one gateway in the path with team and feature attribution, and test its budgets and price table with a hand calculation. Give budgets one request of headroom, use model allow-lists, and alert on anomalies.

Apply the levers in order of risk: output caps first, then a stable prefix for caching, then context trimming, batch for anything asynchronous, then a smaller model or a cascade with a deterministic verifier, and semantic caching last, only with validation. Re-run the eval set after every lever, because they interact. And give finance a FOCUS-shaped export that you reconcile against the invoice.

**Sources:** [workshop-plan.md](workshop-plan.md) (takeaways checklist), [talk-outline.md](talk-outline.md) (segment 10), [AWS Bedrock cost attribution best practices](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-best-practices.html)

## Slide 25 — Questions?
**Timing:** 0:45 (34:15–35:00)
**On slide:**
- Research, gateway comparison, workshop (lever lab, cache probe, semantic-cache stress test, LiteLLM budgets + FOCUS chargeback, self-host break-even — all on free models), this deck and the script
- https://github.com/vusatui/rnd-research/tree/main/ai-finops
- Anton Vusatyi

**Speaker notes:**
Thank you. Everything is in the repo: the research notes with verification markers, the gateway comparison, the workshop you can run with a free OpenRouter key and Docker, this deck and the full script. Happy to take questions.

**Sources:** [README.md](README.md), [workshop-plan.md](workshop-plan.md)

---

## Likely audience questions & answers

Prepared answers. Same facts policy as the slides: stick to the repo; say "vendor claim", "forecast" or "we did not test" where it applies.

**Q1. Prices fall ~13x a year. Why not just wait?**
Because the bill is price × quantity, and quantity grows faster in agentic systems. Epoch's decline is for a *fixed* capability level ✅ ([Epoch](https://epoch.ai/publications/the-plunging-price-of-thought)), while teams move to newer tiers that are priced higher ($10/$50 per 1M ✅) and agents multiply tokens per task. Gartner forecasts cost per agentic workflow up more than fivefold through 2028 🔮; Accenture's respondents would spend price cuts on new use cases 🟡. And promos end: Gemini 4 Argon doubles on 1 Dec 2026 ✅ ([Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)).

**Q2. Isn't 16 tickets too small to conclude anything?**
For quality, yes: one run per configuration, so 14/16 vs 15/16 is noise, and we say so 🧪. For cost, the deltas are driven by token counts that do not flip between runs (403 → 85 output tokens, 4.2k → 1.5k input tokens), so −26% / −68% / −96% hold for *this* prompt shape 🧪. Use the harness as a template and run it on your own eval set, with repeats ([workshop-plan.md](workshop-plan.md)).

**Q3. Which lever should we try first?**
Output caps and a concise format: low effort, and in our run cheaper, faster (p50 8.9 s → 2.3 s) and not visibly worse 🧪. Next, move dynamic values out of the prompt prefix so provider caching can work ✅/🧪. Then context trimming with a retrieval recall check. Smaller models and cascades only with an eval set and a deterministic verifier ([comparison.md §5](comparison.md)).

**Q4. Can prompt caching ever cost more?**
Yes. With a write premium (1.25x on OpenAI GPT-5.6+ and Anthropic 5-min, 2x on Anthropic 1-hour ✅), a prefix written once and never read costs 1.25x-1.99x of no caching 🧪 (simulation, [caching_sim_C_stable.md](workshop/results/caching_sim_C_stable.md)). A timestamp at the top of the prompt makes every request that case. Gemini's implicit caching has no write fee ✅ ([OpenAI caching](https://platform.openai.com/docs/guides/prompt-caching), [Anthropic caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).

**Q5. Is semantic caching safe at a high threshold like 0.95?**
At 0.95 our stress test had 0 wrong hits, but also 0 saved calls 🧪 ([semantic_cache_embeddings.md](workshop/results/semantic_cache_embeddings.md)). vCache shows the optimal threshold varies per item from 0.71 to 1.0 ✅ ([arXiv 2502.03771](https://arxiv.org/abs/2502.03771)), so one global threshold cannot guarantee correctness. Use exact-match caching for safe wins; semantic caching only with per-domain validation, short TTLs, and never for account-specific or numeric answers.

**Q6. Can't we escalate on the model's own low confidence?**
In our run self-reported confidence was ≥0.75 on 15/16 small-model answers, including the invented "$9,900" at 0.95 🧪. A deterministic check (every $ amount must exist in the KB or the ticket) caught it 🧪. Research routers (RouteLLM ✅, FrugalGPT ✅) *learn* an escalation signal from data; a calibrated classifier or a deterministic domain check is the step up, not self-reported confidence.

**Q7. Which gateway should we pick?**
The one your platform team can operate, made the only path to the models ([comparison.md §2](comparison.md)). LiteLLM for self-hosted multi-provider (tested 🧪), the cloud's native option if single-cloud (Bedrock inference profiles, Azure APIM `llm-token-limit` ✅), Cloudflare / Kong / Envoy if you already run them ✅ (docs only). Whatever you pick, trip a budget on purpose and compare its cost numbers with a hand calculation: our LiteLLM setup logged $0 until we changed the provider prefix 🧪.

**Q8. Our budget overshot. Is the gateway broken?**
Probably not. LiteLLM checks the budget before the call using recorded spend, so the crossing request is served (112% in our run) 🧪; Cloudflare documents its spend limits as eventually consistent ✅ ([docs](https://developers.cloudflare.com/ai-gateway/features/spend-limits/)); Azure APIM notes that concurrent requests can exceed the limit ✅ ([docs](https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy)). Size budgets with headroom and treat them as a cap on the tail, not as an exact invoice.

**Q9. How do we attribute cost when one gateway serves many users or agents?**
Stamp low-cardinality tags (team, feature, environment) for billing, keep user and request ids in logs only, and never put PII in tags (AWS guidance ✅, [docs](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-best-practices.html)). FOCUS 1.5's `PrincipalId` says who *made* the call, not who *benefits* ✅, and the FinOps Foundation says there is no generally accepted framework for multi-agent allocation yet ✅. Agree an allocation rule with finance and start with showback.

**Q10. Is FOCUS ready for AI chargeback today?**
FOCUS 1.4 is published and carries token quantities ✅; the AI-specific columns (ModelId, TokenDirection, TokenCacheAction, PrincipalId) are in the 1.5 working draft, ratification planned 3 Dec 2026 ✅ ([scope](https://focus.finops.org/focus-1-5-release-scope/)). Until providers emit them, shape your gateway logs like FOCUS; ours ([to_focus.py](workshop/ex4_gateway/to_focus.py)) was not run through the FOCUS validator 🧪.

**Q11. When does self-hosting pay off?**
On our stated assumptions, at ~64% sustained utilization versus an open-weights model bought via API and ~18% versus a frontier price (a different model and quality) 🧪; at ~$10/GPU-h the first never breaks even 🧪 ([breakeven_default.md](workshop/results/breakeven_default.md)). GPU prices are secondary 🟠 and throughput is our assumption. Business-hours traffic caps an always-on replica at ~30%. Residency, latency and model control are often the real reasons; price them separately.

**Q12. Is "token cost engineering" a new discipline or FinOps plus performance engineering?**
That is listed as disputed in [research.md §9](research.md). The FinOps Foundation treats AI as an extension of FinOps (Price × Quantity, allocation, KPIs ✅); the token-level levers (caching, routing, trimming, verifiers) are engineering work inside the application. Services firms now name it as an offering (EPAM Q2 2026 earnings call 🟡). In practice it needs both: finance's allocation model and engineers who can change prompts and measure quality.

**Q13. Do the McKinsey "30x tokens" and "4x pilot to production" numbers hold?**
They are quotes from an expert interview with no published dataset 🟡 ([McKinsey](https://www.mckinsey.com/featured-insights/mckinsey-explainers/what-does-ai-really-cost)). Use them as illustrations of the mechanism (statelessness, retries, sub-agents), not as benchmarks. Measure your own tokens per task instead.
