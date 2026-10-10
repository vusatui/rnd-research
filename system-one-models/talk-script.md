# Talk script: "System One Models: when AI should decide, not write" (~35 min)

25 slides, 35:00 of planned speaking time including Q&A. The HTML deck is in [`slides/index.html`](slides/index.html). Its speaker notes are built from this file by `slides/build_notes.py`, so edit the notes here first.

**Facts policy.** Every fact comes from [`research.md`](research.md), [`comparison.md`](comparison.md), [`talk-outline.md`](talk-outline.md) and [`workshop-plan.md`](workshop-plan.md) (our own runs, 2026-10-10), plus the code in [`workshop/`](workshop/). Markers follow research.md: ✅ verified on a primary page on 2026-10-10, 🟡 vendor-only claim (the vendor about itself, not reproduced), 🟠 secondary source only, ❌ conflicting or unverified. Say 🟡/🟠/❌ items out loud as claims, not as facts. Benchmarks in this talk are vendor-run unless they are ours.

**Presenter keys (deck):** → / Space / PageDown next, ← / PageUp back, Home / End, `N` notes overlay, `S` speaker window (notes, next slide, timer), `O` overview, `F` fullscreen.

| # | Slide | Time | Ends at |
|---|---|---|---|
| 1 | System One Models: when AI should decide, not write | 0:30 | 0:30 |
| 2 | Why are we generating prose to make a yes/no decision? | 1:30 | 2:00 |
| 3 | System 1 and System 2, in software | 1:30 | 3:30 |
| 4 | Intuition plus deliberation is an old idea | 1:15 | 4:45 |
| 5 | September–October 2026: a product category appears | 1:45 | 6:30 |
| 6 | Jev by TypeSafe AI | 1:45 | 8:15 |
| 7 | Check the source: the Jev look-alike sites | 1:00 | 9:15 |
| 8 | OpenAI Decisions API (public beta) | 1:45 | 11:00 |
| 9 | The open side: Cloudflare Clef, Laya, Liquid d1 | 1:45 | 12:45 |
| 10 | Train your own: the Unsloth recipe | 1:30 | 14:15 |
| 11 | Anatomy of a decision call | 1:30 | 15:45 |
| 12 | Three primitives, two wire formats | 1:45 | 17:30 |
| 13 | Under the hood: read once, score every option | 1:15 | 18:45 |
| 14 | Probability, confidence and calibration | 1:45 | 20:30 |
| 15 | It's not new: the System 1 family | 1:30 | 22:00 |
| 16 | Ways to make a System 1 decision | 1:30 | 23:30 |
| 17 | Decision-model APIs side by side | 1:15 | 24:45 |
| 18 | Pattern: the confidence-gated cascade | 1:30 | 26:15 |
| 19 | More patterns: fan-out, composite scores, guardrails, tool selection | 1:30 | 27:45 |
| 20 | Live demo: the workshop | 0:45 | 28:30 |
| 21 | Classifier vs LLM-as-decider: what we measured | 1:45 | 30:15 |
| 22 | The cascade: one threshold, two numbers | 1:30 | 31:45 |
| 23 | Pitfalls and checklist | 1:30 | 33:15 |
| 24 | Takeaways | 0:45 | 34:00 |
| 25 | Questions? | 1:00 | 35:00 |

---

## Slide 1 — System One Models: when AI should decide, not write
**Timing:** 0:30 (0:00–0:30)
**On slide:**
- Title: System One Models: when AI should decide, not write
- Subtitle: Jev, OpenAI Decisions, Cloudflare Clef, the Unsloth recipe, and the decision models we already had
- Anton Vusatyi · R&D · October 2026
- Repo: github.com/vusatui/rnd-research → system-one-models

**Speaker notes:**
Hi, I'm Anton. This talk is about a new kind of model that does not write text at all. It reads an input and returns a decision with a probability. In September and October 2026 several vendors shipped such models. I will show what they are, how they work, how they relate to classifiers and rerankers we have used for years, and what we measured ourselves in a small workshop. Facts were checked on October 10, 2026. Everything is in the public repo on the slide, with sources. When something is only a vendor claim, I will say so.

## Slide 2 — Why are we generating prose to make a yes/no decision?
**Timing:** 1:30 (0:30–2:00)
**On slide:**
- Same support ticket: "I was charged twice for my March invoice and nobody answers. Refund today please."
- Path A, generative LLM: prompt → a paragraph (or JSON) → parse → hope it is one of the labels. Our ex2 run: ~1.3 s median per ticket (free 120B model, k=3 samples)
- Path B, decision model: state + question → `{"route": "billing", p, confidence}`. Jev median 524 ms in Cloudflare's test 🟡; our TF-IDF classifier 0.6 ms
- Question: most production AI calls are snap judgments consumed by code

**Speaker notes:**
Here is the same support ticket handled two ways. This is the ticket from our workshop: charged twice, nobody answers, refund today.

Path A is what most of us do today. We send it to a chat LLM, ask it to pick a team, get back text or JSON, parse it, and hope the answer is one of our labels. In our own run with a free 120-billion-parameter model on OpenRouter, sampling three answers per ticket to get a probability, the median was about 1.3 seconds per ticket.

Path B is a decision model. We send the ticket as state and a typed question, "which team owns this, one of five", and get back a choice, a probability and a confidence. No text to parse. Cloudflare measured Jev at a median of 524 milliseconds. That is Cloudflare's benchmark, not ours. And a plain classifier that we trained in the workshop answers in 0.6 milliseconds.

So the question for this talk: why do we generate prose when the consumer of the answer is an if statement?

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-10), [workshop/ex4_decision_apis/compare.py](workshop/ex4_decision_apis/compare.py), [Cloudflare blog: Clef](https://blog.cloudflare.com/clef-decision-models/) (Jev 524 ms, vendor benchmark)

## Slide 3 — System 1 and System 2, in software
**Timing:** 1:30 (2:00–3:30)
**On slide:**
- Kahneman, *Thinking, Fast and Slow*: System 1 is fast and intuitive, System 2 is slow and deliberate
- TypeSafe named its model class after it ("System One") ✅
- Software mapping: an LLM writing text is System 2 (slow, verbal reasoning); classify, route, gate, rank are System 1
- System 1 output is a typed decision with a probability, read by code, not by a person

**Speaker notes:**
The name comes from Daniel Kahneman's book Thinking, Fast and Slow. System 1 is fast, automatic, intuitive. System 2 is slow, deliberate, effortful. TypeSafe explicitly says that is where the name "System One model" comes from.

Map this to software. A large language model that writes an answer token by token is System 2: verbal reasoning, slow and expensive. But look at what most production AI calls actually do. Is this spam? Which queue does this ticket go to? Is this prompt an injection? Which of these ten documents is most relevant? Which tool should the agent call? Those are snap judgments. Their output is not prose for a human. It is a typed value that code branches on.

A System 1 model gives you exactly that: a choice, a score or a yes-probability, and ideally an honest estimate of how sure it is.

**Sources:** [TypeSafe docs: System One](https://docs.typesafe.ai/concepts/system-one), [talk-outline.md](talk-outline.md)

## Slide 4 — Intuition plus deliberation is an old idea
**Timing:** 1:15 (3:30–4:45)
**On slide:**
- AlphaGo: a policy network proposes moves ("intuition"), Monte Carlo tree search checks them ("deliberation")
- Production AI has the same shape: a fast judge for most inputs, a slow reasoner for the hard ones
- The new part is not the split. It is a general, zero-shot System 1 with a standard API

**Speaker notes:**
This split is not new in AI. AlphaGo is the classic example. A policy network looks at the board and proposes promising moves almost instantly. That is intuition. Then tree search spends compute checking a few of those moves in depth. That is deliberation. Neither alone was enough.

Production systems want the same shape. A fast, cheap judge handles the bulk of inputs. Only the uncertain, high-stakes cases go to the slow reasoner or a human. We will build exactly this as a cascade later in the talk.

What is new in the autumn of 2026 is not the split. It is that you can now get a general-purpose, instruction-following System 1 model that works zero-shot on your own labels, behind a standard API. That is the news part, next.

**Sources:** [research.md §4](research.md), [talk-outline.md](talk-outline.md)

## Slide 5 — September–October 2026: a product category appears
**Timing:** 1:45 (4:45–6:30)
**On slide:**
- Timeline: Jev launch reported 15 Sep 🟠 · Cloudflare Clef on Workers AI, changelog 2026-10-01 ✅ · OpenAI Decisions API public beta, announced 6–7 Oct 🟠 (beta itself ✅) · Unsloth "train your own decision model like Jev", 2026-10-07 ✅
- Also: Laya (Convai Innovations, open weights 🟠), Liquid d1 (availability ❌ conflicting)
- Legend: ✅ verified on a primary page · 🟡 vendor-only · 🟠 secondary only · ❌ conflict

**Speaker notes:**
Here is the timeline, with the honesty markers I will use for the rest of the talk. Green check: I read it on the vendor's or official page. Yellow: the vendor says it about itself. Orange: only third-party sources. Red: sources conflict.

TypeSafe's Jev launched in mid-September. The date of 15 September comes only from secondary sources; I could not find it on a TypeSafe page. On October 1, Cloudflare's changelog announced Clef on Workers AI, with open weights. That one is verified. Around October 6 and 7, OpenAI put a Decisions API into public beta. The beta and its docs are verified; the exact announcement date comes from a community thread and a blog. And on October 7, Daniel Han from Unsloth posted that you can now train your own decision model like Jev locally. That is the LinkedIn post that started this research.

Two more names appear in the tables: Laya from Convai Innovations, an open encoder model, known only from third-party pages and Unsloth's docs, and Liquid AI's d1, where sources disagree on whether you can self-host it.

**Sources:** [research.md §1–4](research.md), [Cloudflare changelog 2026-10-01](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/), [OpenAI Decisions guide](https://platform.openai.com/docs/guides/decisions), [LinkedIn post (Daniel Han, Unsloth)](https://lnkd.in/p/e9nNGmzZ)

## Slide 6 — Jev by TypeSafe AI
**Timing:** 1:45 (6:30–8:15)
**On slide:**
- "First System One model": returns typed decisions and probabilities; no replies, code or explanations ✅
- `POST https://api.typesafe.ai/v1/systemone` with `model`, `state`, `questions` (map); SDKs `typesafe-sdk`, `@typesafe-ai/sdk` ✅
- `jev-1.13.0` (aliases `jev-latest`, `jev-preview`) · $0.042 / 1M input tokens, output free · 64k context · 100K tok/s, 80 req/s ✅
- Text only; English best; same weights for every account, no per-customer fine-tuning ✅
- Trained for calibration ("RLCD", not explained in detail) · parameter count not published
- Founders, $40M seed, "70–500 ms": secondary sources only 🟠

**Speaker notes:**
Jev is TypeSafe's flagship. Their docs call it the first System One model. It returns typed decisions and probabilities. It does not write replies, code or explanations of its reasoning.

The API is one endpoint, slash v1 slash systemone. You send a model name, a state, and a map of named questions. There are Python and JavaScript SDKs. The current model is jev 1.13.0, and both jev-latest and jev-preview point to it today. Price: 4.2 cents per million input tokens, output is free. 64k context per request. Rate limits are 100 thousand tokens or 80 requests per second, and TypeSafe says they adjust dynamically because of demand.

Limits that matter: text only, no images yet. English works best. Every account gets the same weights; there is no customer fine-tuning, and they say they do not train on customer data. They say the model is trained for calibration with a method they call RLCD, which the pages I read do not explain. No parameter count is published.

Founders, funding and the popular "70 to 500 milliseconds" latency figure come only from unofficial sites. Treat them as rumors.

**Sources:** [TypeSafe: System One](https://docs.typesafe.ai/concepts/system-one), [TypeSafe: Models](https://docs.typesafe.ai/models.md), [TypeSafe: Confidence](https://docs.typesafe.ai/confidence.md), [research.md §1](research.md)

## Slide 7 — Check the source: the Jev look-alike sites
**Timing:** 1:00 (8:15–9:15)
**On slide:**
- Within weeks: jevtypesafeai.com, jevai.guide, jevwiki.ai, madewithjev.com, systemonemodels.ai, modelsystem.one … — none of them is TypeSafe
- Example: unofficial price $0.42 / 1M ❌ vs official $0.042 / 1M ✅ (10× off)
- We treat only `docs.typesafe.ai` as primary for Jev
- Rule for hype cycles: vendor docs for facts, independent tests for quality, your own data for decisions

**Speaker notes:**
A practical warning. In the weeks after launch, a whole cloud of unofficial Jev sites appeared: jevtypesafeai dot com, jevai dot guide, jevwiki, madewithjev and more. None of them is TypeSafe, and some contradict the official docs.

The clearest example is price. One of them says 42 cents per million tokens. The official Models page says 4.2 cents. That is a factor of ten. If you build a cost model from a search snippet, you can be off by an order of magnitude.

So my rule for this research, and I recommend it for any hype cycle: only the vendor's own docs count as a source for product facts. Quality claims need independent tests. And decisions about your system need your own labeled data.

**Sources:** [research.md §1](research.md) (caution box and pricing conflict), [TypeSafe: Models](https://docs.typesafe.ai/models.md)

## Slide 8 — OpenAI Decisions API (public beta)
**Timing:** 1:45 (9:15–11:00)
**On slide:**
- `POST /v1/decisions` with `model`, `input`, `questions` (array, each with `name`) → `answers` array; a `refusal` answer type exists ✅
- One model: `gpt-6-luna` · question types `predicate`, `choice`, `score` ✅
- Text and images (base64 data URLs only) ✅
- $0.10 / 1M input tokens; no output or cache charges ✅ · "about 10× faster than the Responses API" 🟡
- ZDR and HIPAA for eligible customers, US/EU residency · SDK: Python 3.26.0+, JS 7.30.0+ (`client.decisions.create`) ✅
- OpenAI: use Structured Outputs / function calling when you need generated objects ✅ · also on Vercel AI Gateway 🟡

**Speaker notes:**
OpenAI's version is the Decisions API, in public beta, with general availability promised "in the coming weeks". The endpoint is slash v1 slash decisions. You send a model, an input, and an array of questions, each with a name. You get back an array of answers, and there is a refusal answer type.

There is exactly one model, gpt-6-luna. Question types are predicate, which is a yes-probability, choice, and score. Unlike Jev, it accepts images, but only as base64 data URLs, not hosted URLs or file IDs.

Price is 10 cents per million input tokens, with no output or cache charges. OpenAI says it is about ten times faster than the Responses API. That is their claim; I have not measured it. For enterprises: zero data retention and HIPAA for eligible customers, and US or EU data residency.

Note one honest line in OpenAI's own guide: if you need a generated object or tool arguments, use Structured Outputs or function calling instead. Decisions is for decisions. Vercel's changelog says its AI Gateway serves this API too, and also routes Jev, Liquid d1 and Laya through the same endpoint.

**Sources:** [OpenAI Decisions guide](https://platform.openai.com/docs/guides/decisions), [Vercel changelog](https://vercel.com/changelog/openai-decisions-api-now-available-on-ai-gateway), [research.md §2](research.md)

## Slide 9 — The open side: Cloudflare Clef, Laya, Liquid d1
**Timing:** 1:45 (11:00–12:45)
**On slide:**
- **Clef** (27B) and **Clef-flash** (9B), Cloudflare: open weights, Apache 2.0, Workers AI `@cf/cloudflare/clef(-flash)`, 64K context ✅; "fully Jev-API compatible" 🟡
- Cloudflare's own benchmark: leads 7 of 10 decision benchmarks; median 209 ms / 39 ms vs Jev 524 ms 🟡
- **Laya** (Convai Innovations): ModernBERT-large encoder + decision head, ~0.4B, Apache 2.0; needs fine-tuning 🟠
- **Liquid d1 / d1-3B**: LFM Open License; hosted-only vs self-hostable ❌ conflicting

**Speaker notes:**
Now the open side. Cloudflare released Clef, 27 billion parameters, and Clef-flash, 9 billion, with open weights under Apache 2.0, and runs them on Workers AI with 64k context. They describe them as fully Jev-API compatible. That is their claim; our workshop code assumes it but I could not test the exact request body.

Cloudflare also published a benchmark: Clef leads seven of ten decision benchmarks, with median latency of 209 milliseconds for Clef and 39 for Clef-flash, versus 524 for Jev. Remember who ran it. It is a vendor comparing itself with a competitor.

Laya, from Convai Innovations, is the small end: a ModernBERT-large encoder with a decision head, about 0.4 billion parameters, Apache 2.0, very fast, but it needs fine-tuning to be useful. That comes from third-party pages and Unsloth's docs only.

Liquid AI's d1 is the open question. Sources disagree on whether d1 is hosted-only or self-hostable. d1-3B is under Liquid's open license, which restricts commercial use above 10 million dollars revenue. Check Liquid's own page before you plan on it.

**Sources:** [Cloudflare changelog](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/), [Cloudflare blog: Clef](https://blog.cloudflare.com/clef-decision-models/), [Unsloth: Laya](https://unsloth.ai/docs/models/decision-laya), [research.md §4](research.md)

## Slide 10 — Train your own: the Unsloth recipe
**Timing:** 1:30 (12:45–14:15)
**On slide:**
- Daniel Han (Unsloth), LinkedIn, 2026-10-07: "train your own Decision model like Jev locally" ✅
- New `FastDecisionModel` / `DecisionTrainer`: the LLM reads input + all questions/options once; a small scoring head scores every option ("same design as Cloudflare's Clef") ✅
- Claims: Qwen3.5 0.8B from 20.7% to 74.3% across 3 decision benchmarks on 4 GB VRAM; LoRA r=64, one epoch, 30–37% → 78% 🟡
- Free Colab/Kaggle notebooks (Qwen3.5-4B); serve as a Jev-compatible API (`jev-latest` → your model) ✅
- Also: serve Laya locally behind a TypeSafe-compatible API; Laya's `confidence` formula differs from Jev's ✅

**Speaker notes:**
The post that triggered this research is from Daniel Han at Unsloth, October 7. The claim: you can now train your own decision model like Jev, locally.

Unsloth added a FastDecisionModel and a DecisionTrainer. The design: the language model reads the input plus all questions and options once, and a small scoring head scores every option. Unsloth says it is the same design as Cloudflare's Clef. No text generation at all.

The numbers in the post: Qwen 3.5 0.8B went from 20.7 to 74.3 percent accuracy across three decision benchmarks, on only 4 gigabytes of VRAM. And with a LoRA of rank 64 for one epoch, downstream accuracy went from 30 to 37 percent up to 78. Those are Unsloth's numbers, not reproduced.

What I find most interesting: they ship free Colab and Kaggle notebooks, and the trained model can be served behind a Jev-compatible API, so a request for jev-latest goes to your model. They also show Laya served behind a TypeSafe-compatible API, with an important caveat: Laya computes confidence differently from Jev. Same field name, different meaning.

**Sources:** [LinkedIn post](https://lnkd.in/p/e9nNGmzZ), [Unsloth guide](https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth), [Unsloth: Laya](https://unsloth.ai/docs/models/decision-laya), [research.md §3](research.md)

## Slide 11 — Anatomy of a decision call
**Timing:** 1:30 (14:15–15:45)
**On slide:**
- Diagram: state (ticket text / JSON) + typed questions → decision model (one pass) → answers: probabilities + confidence
- Input: a state plus several named questions in one request
- Output: typed answers, never free text; billed on input tokens only
- Converging shape across Jev, OpenAI, Clef, Unsloth, Vercel gateway

**Speaker notes:**
Let's open the box. Every one of these APIs has the same anatomy.

On the left, the state: the thing you are deciding about. A ticket, a JSON object, a chat transcript. Next to it, a set of named, typed questions. Which team? Is it urgent? How frustrated is the customer? All in one request.

The model reads all of that once and returns typed answers: a probability for a yes-no question, a probability per option for a choice, a level for a score, plus a confidence. Never free text. Because there is no generated output, the vendors bill only input tokens. Output is free at TypeSafe and OpenAI.

The shape is converging. Jev, OpenAI, Clef, Unsloth's served models and Vercel's gateway all speak a variant of state plus typed questions in, probabilities and confidence out. Research.md calls the Jev-compatible API a de facto interface in the making, the way the OpenAI chat API became the standard for LLMs.

**Sources:** [research.md §5](research.md), [TypeSafe: System One](https://docs.typesafe.ai/concepts/system-one), [OpenAI Decisions guide](https://platform.openai.com/docs/guides/decisions)

## Slide 12 — Three primitives, two wire formats
**Timing:** 1:45 (15:45–17:30)
**On slide:**
- Jev: Noul (probability of "yes") · Choice (one of N) · Score (ordered levels) ✅
- OpenAI: predicate · choice (value + probabilities + confidence) · score (probability-weighted average of level indices + confidence) ✅
- Jev: `state` + `questions` **map** · OpenAI: `input` + `questions` **array** with `name`
- Code side by side, from our `ex4_decision_apis/compare.py`
- Limits seen on Vercel docs: 1–255 choices, 2–10 score levels 🟡

**Speaker notes:**
Both big vendors landed on the same three primitives.

One: a yes-probability. TypeSafe calls it Noul, OpenAI calls it predicate. Two: choice, pick one of N options, with a probability for each. Three: score, an ordered scale like low, medium, high. OpenAI defines the score answer as a probability-weighted average of level indices, plus a confidence.

The wire formats differ in small, annoying ways. Jev takes a state and a map of questions keyed by name. OpenAI takes an input and an array of questions, each carrying its own name, and choices are objects with a value. On the slide is the same ticket with the same two questions in both formats, straight from our exercise 4 code.

Vercel's docs list limits of 1 to 255 choices and 2 to 10 score levels. I did not see those on OpenAI's own page, so treat them as Vercel's.

The practical point: write a thin adapter once, and you can switch vendors or point to a self-hosted Clef or Unsloth model.

**Sources:** [TypeSafe: System One](https://docs.typesafe.ai/concepts/system-one), [OpenAI Decisions guide](https://platform.openai.com/docs/guides/decisions), [workshop/ex4_decision_apis/compare.py](workshop/ex4_decision_apis/compare.py), [research.md §2](research.md)

## Slide 13 — Under the hood: read once, score every option
**Timing:** 1:15 (17:30–18:45)
**On slide:**
- Generative LLM: decode token by token, then parse; probabilities need logprobs or k samples
- Decision model: encode state + questions + options once → scoring head → a probability per option. No decoding loop.
- Consequence: output tokens are free; latency is one forward pass
- Exact architectures of Jev and gpt-6-luna are not published; the "read once + scoring head" design is what Unsloth and Cloudflare describe

**Speaker notes:**
Why is this faster and why can output be free? A generative LLM produces its answer token by token and then you parse it. If you want a probability, you either read logprobs or sample several answers and count votes, which is what our exercise 2 does.

A decision model, at least in the design Unsloth and Cloudflare describe, reads the state, the questions and all options once, and a small scoring head assigns a score to every option. There is no decoding loop. Latency is roughly one forward pass, and there is nothing to bill as output.

I want to be careful here. TypeSafe and OpenAI do not publish their architectures, and TypeSafe publishes no parameter count. The read-once-plus-scoring-head picture is what Unsloth documents, and what they say Clef does. For the closed models, it is a reasonable mental model, not a known fact.

**Sources:** [Unsloth guide](https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth), [workshop/decider.py](workshop/decider.py), [research.md §1, §3](research.md)

## Slide 14 — Probability, confidence and calibration
**Timing:** 1:45 (18:45–20:30)
**On slide:**
- Jev and OpenAI return **confidence** separately from **probability**; designed for "act vs escalate to a human or reasoning model" ✅
- Calibrated = "when it says 80%, it is right about 80% of the time" — a property of a group of answers, not a per-answer guarantee ✅ (TypeSafe)
- ECE: bin answers by confidence, average |accuracy − confidence| weighted by bin size (our `common.py`, 5 bins)
- Diagram: reliability chart (illustration, not data)
- Calibration quality is a vendor claim 🟡 — measure it on your labels

**Speaker notes:**
This slide is the reason these models exist. They return a probability, and separately a confidence. TypeSafe says the design goal is exactly the decision "act on this, or escalate to a human or a reasoning model".

A probability is only useful if it is calibrated. Calibrated means: of all the answers where the model said 80 percent, about 80 percent are right. TypeSafe makes an important point in its docs: calibration is a property of a group of answers. It is not a guarantee for any single answer.

How do you measure it? Expected Calibration Error. Sort answers into bins by confidence. In each bin, compare the average confidence with the actual accuracy. Average the gaps, weighted by how many answers fall in each bin. Zero is perfect. Our workshop's common.py does this with five bins in about ten lines.

The chart is an illustration of what a reliability diagram looks like, not data. And whether a vendor's model is well calibrated on your data is a vendor claim until you measure it. OpenAI's own guide says the same.

**Sources:** [TypeSafe: System One](https://docs.typesafe.ai/concepts/system-one), [TypeSafe: Confidence](https://docs.typesafe.ai/confidence.md), [workshop/common.py](workshop/common.py), [research.md §5](research.md)

## Slide 15 — It's not new: the System 1 family
**Timing:** 1:30 (20:30–22:00)
**On slide:**
- Text classifiers: logistic regression, fine-tuned BERT / ModernBERT
- Cross-encoder rerankers · reward models / LLM-as-judge
- Embedding similarity + kNN (semantic routing)
- LLM routers (e.g. RouteLLM) · guardrail classifiers (Llama Guard-style)
- RL policy / value networks (AlphaGo)
- New in Sept–Oct 2026: **general-purpose, instruction-following, zero-shot**, with a standard API

**Speaker notes:**
Now the generalization. If a System 1 model is anything that reads an input and returns a typed decision with a probability, then we have had them for years.

A logistic regression spam filter is one. A fine-tuned BERT or ModernBERT classifier is one. The cross-encoder reranker in your RAG pipeline that scores query-document pairs is one. Reward models in RLHF and LLM-as-judge setups are decision models. Embedding similarity with nearest neighbours is how many semantic routers work. LLM routers like RouteLLM decide which model gets a request. Guardrail classifiers in the Llama Guard style decide whether a prompt or response is unsafe. And in reinforcement learning, policy and value networks are the System 1 of the agent.

What is new is one thing: a general-purpose, instruction-following model that you can ask a new question zero-shot, without training data, and get calibrated probabilities back, behind a standard API. Before, every new label meant collecting data and training a model.

**Sources:** [research.md §4](research.md) ("older, well-established members of the same class")

## Slide 16 — Ways to make a System 1 decision
**Timing:** 1:30 (22:00–23:30)
**On slide:**
- Table (from comparison.md): approach · latency · calibrated probabilities · needs labeled data · zero-shot new labels · example
- Rules/regex µs · TF-IDF + LR µs–ms (ex1) · fine-tuned encoder ms · embeddings + kNN ms · reranker / reward model 10–100 ms · **general decision model 10–500 ms, trained for calibration, zero-shot** · LLM + constrained output 0.3–3 s (ex2) · reasoning LLM seconds–minutes (ex3 escalation)

**Speaker notes:**
Here is the whole family on one table, from our comparison. Read it top to bottom as a ladder from cheapest to most flexible.

Rules and regex: microseconds, no probabilities, no new labels without code. A classic classifier like TF-IDF plus logistic regression: microseconds to milliseconds, rough probabilities that can be recalibrated, but it needs labeled data and cannot learn a new label zero-shot. That is our exercise 1. Fine-tuned encoders, embeddings with nearest neighbours, rerankers and reward models sit in the middle.

The general decision model row is the new one: 10 to 500 milliseconds, trained for calibration, no labeled data needed, new labels zero-shot. Below it, an LLM with constrained output: 0.3 to 3 seconds, poor probabilities unless you sample or read logprobs. That is exercise 2. And at the bottom, a reasoning LLM, seconds to minutes, which is our escalation path in exercise 3.

The latency ranges are rough orders of magnitude from our comparison, not benchmarks. The point is the shape: decision models fill the gap between "train a classifier" and "call an LLM".

**Sources:** [comparison.md](comparison.md) ("Broader class")

## Slide 17 — Decision-model APIs side by side
**Timing:** 1:15 (23:30–24:45)
**On slide:**
- Table (from comparison.md): Jev 1.13 · OpenAI Decisions · Clef / Clef-flash · Laya — access, endpoint, input, price per 1M input tokens, size, median latency, customization
- Jev: hosted, text only, $0.042, size not published, 524 ms (Cloudflare's test 🟡), no customization
- OpenAI: hosted beta, text + images, $0.10, "~10× faster than Responses" 🟡
- Clef: Workers AI + open weights, 27B / 9B, $0.24 / $0.09 🟠, 209 / 39 ms 🟡, open weights
- Laya: open weights 🟠, ~0.4B, ~6–40 ms 🟡, fine-tune required · Liquid d1: ❌ conflicting

**Speaker notes:**
And the new products side by side. I will not read the whole table; look at the markers.

The hosted pair, Jev and OpenAI, have verified prices: 4.2 and 10 cents per million input tokens, output free. Jev is text only; OpenAI takes images. Neither lets you customize the model beyond the prompt and the state.

Clef is the open option with a verified size, 27 and 9 billion parameters, but its Workers AI prices come from a secondary source, and its latency is Cloudflare's own measurement. Laya is the tiny, fast one, but needs fine-tuning, and everything about it is secondary. Liquid's d1 is too unclear to put numbers on.

Notice how many latency cells are yellow. There is no independent benchmark across these providers yet. If latency or calibration matters to you, you will have to measure them yourself.

**Sources:** [comparison.md](comparison.md) ("Decision-model APIs"), [research.md](research.md)

## Slide 18 — Pattern: the confidence-gated cascade
**Timing:** 1:30 (24:45–26:15)
**On slide:**
- Diagram: request → System 1 (classifier / decision model) → confidence ≥ threshold? yes → act · no → System 2 (reasoning LLM) → still unsure → human queue
- Threshold is the dial between cost/latency and accuracy
- Thresholds depend on the model version: pin it
- Our ex3 implements this in ~40 lines (`--no-llm` sends escalations to a "human" queue)

**Speaker notes:**
The most important architecture pattern is the confidence-gated cascade. A request first goes to a System 1 model: a classifier or a decision model. If its confidence is above a threshold, we act on the answer immediately. Fast and cheap. If not, we escalate: to a reasoning LLM, and if that is still unsure, or the stakes are high, to a human queue.

The threshold is one dial. Turn it up and you escalate more: higher accuracy, more cost and latency. Turn it down and System 1 handles more on its own.

Two practical notes. First, a threshold tuned for one model version may be wrong for the next. This is why you pin versions instead of using latest. Second, this is small code. Our exercise 3 is about forty lines, and we will look at its numbers in the demo.

**Sources:** [workshop/ex3_cascade/cascade.py](workshop/ex3_cascade/cascade.py), [talk-outline.md](talk-outline.md), [TypeSafe: System One](https://docs.typesafe.ai/concepts/system-one) (act vs escalate)

## Slide 19 — More patterns: fan-out, composite scores, guardrails, tool selection
**Timing:** 1:30 (26:15–27:45)
**On slide:**
- **Fan-out:** many named questions about one state in one call (route + urgent + frustration) — input read once, output free
- **Composite scoring in code:** combine probabilities with your own weights and rules, e.g. escalate if p(urgent) × p(VIP) is high
- **Guardrails in and out:** a yes-probability "is this a prompt injection?" before the LLM, "does this leak PII?" after it
- **Agent tool / skill selection:** a choice question over available tools before the expensive reasoning step

**Speaker notes:**
Four more patterns from the outline.

Fan-out. Because the APIs take many named questions per request, you can ask everything you want to know about a ticket in one call: which team, is it urgent, how frustrated. The input is read once and output is free, so extra questions are cheap.

Composite scoring. Because you get numbers instead of prose, you can combine them in plain code with your own weights and business rules. The model gives probabilities; your code owns the policy.

Guardrails. A yes-probability question like "is this a prompt injection?" in front of an LLM, and "does this response leak personal data?" after it. That is a classic guardrail-classifier job, now zero-shot. It is also one of our workshop stretch goals.

Tool or skill selection in agents. Before an agent spends a reasoning step, a choice question over the available tools can pick the likely one, or narrow the list. I have not measured any of these patterns. They are designs, and you should test them on your own data.

**Sources:** [talk-outline.md](talk-outline.md) §6, [workshop-plan.md](workshop-plan.md) (stretch goals), [workshop/decider.py](workshop/decider.py)

## Slide 20 — Live demo: the workshop
**Timing:** 0:45 (27:45–28:30)
**On slide:**
- ex1 classic System 1: TF-IDF + logistic regression (CPU only)
- ex2 LLM as decider: Jev-shaped `choice / score / noul` over a free OpenRouter model; probabilities by k-sample voting
- ex3 confidence-gated cascade (`--no-llm` or OpenRouter)
- ex4 real decision APIs: Jev / OpenAI / Clef — paid keys, no free tier found
- Data: 40 synthetic support tickets (department + urgency) · fallback: recorded numbers on the next slides

**Speaker notes:**
Now the demo, from the workshop folder. Exercise 1 trains a TF-IDF plus logistic regression classifier on CPU. Exercise 2 wraps a free chat model on OpenRouter in the same Jev-shaped API, with choice, score and noul, and estimates probabilities by sampling k answers and counting votes. Exercise 3 is the cascade. Exercise 4 sends the same ticket to Jev, OpenAI and Clef, but it needs paid keys, and I found no free tier for any of them, so today it is a code walkthrough only.

The data is 40 synthetic support tickets labeled with department and urgency. If the free model or the network fails, the next two slides have the numbers we recorded on October 10.

**Sources:** [workshop-plan.md](workshop-plan.md), [workshop/README.md](workshop/README.md)

## Slide 21 — Classifier vs LLM-as-decider: what we measured
**Timing:** 1:45 (28:30–30:15)
**On slide:**
- Table, measured 2026-10-10 on our box:
- ex1 TF-IDF + LR, leave-one-out on 40 tickets: accuracy 40%, ECE 0.055, latency 0.6 ms
- ex2 `nvidia/nemotron-3-super-120b-a12b:free`, k=3, 10 tickets: accuracy 70%, ECE 0.17, ~1.3 s median
- Reading: the LLM knows more (zero-shot), the classifier knows how sure it is
- Caveat: tiny toy dataset, different test sets — the lesson is the trade-off, not the numbers

**Speaker notes:**
Here is what we measured on October 10.

The classifier, evaluated with leave-one-out on all 40 tickets, gets 40 percent accuracy. That is low, because 40 examples over five departments is almost nothing. But look at the calibration: ECE 0.055. When it is unsure, it says so. And it answers in 0.6 milliseconds.

The free LLM, Nemotron 3 Super 120B, three samples per ticket, on the first 10 tickets: 70 percent accuracy, because it understands language without training data. But ECE is 0.17, three times worse, because three votes can only produce confidences of one third, two thirds or one. And the median is about 1.3 seconds per ticket, more than two thousand times slower.

This is exactly the gap that general decision models claim to close: LLM-level understanding with classifier-level speed and calibration. Whether they do is a vendor claim we could not test without paid keys.

The honest caveat: this is a deliberately tiny dataset, and the two runs used different test sets. The lesson is the trade-off, not the numbers.

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-10), [workshop/ex1_classic_baseline/baseline.py](workshop/ex1_classic_baseline/baseline.py), [workshop/ex2_llm_as_decider/run.py](workshop/ex2_llm_as_decider/run.py)

## Slide 22 — The cascade: one threshold, two numbers
**Timing:** 1:30 (30:15–31:45)
**On slide:**
- ex3 without LLM, train on 24 tickets, test on 16: threshold 0.5 → **88% accuracy, 12 of 16 escalated**
- The "human" is assumed always right, so most of the 88% is the human: System 1 alone handled 4 tickets
- The real metric pair: accuracy **and** escalation rate; sweep the threshold and plot both
- `for t in 0.3 0.5 0.7 0.9; do python cascade.py --no-llm --threshold $t | tail -1; done`

**Speaker notes:**
Exercise 3, the cascade, without an LLM. We train the classifier on 24 tickets and test on 16. Low-confidence answers go to a "human" queue.

At a threshold of 0.5, we get 88 percent accuracy with 12 of 16 tickets escalated. Sounds great, until you read the code: the simulated human is assumed always right. So 12 of the 14 correct answers came from the human, and the classifier handled only 4 tickets on its own. With a classifier trained on 24 examples, that is expected.

This is the lesson I want you to take from the demo: a cascade has two numbers, not one. Accuracy and escalation rate. Every escalation costs money or a person's time. So you sweep the threshold, plot accuracy against escalation rate, and pick the point your budget allows. The one-liner on the slide does the sweep. A better System 1 moves the whole curve, and that is where a calibrated decision model should pay off.

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-10), [workshop/ex3_cascade/cascade.py](workshop/ex3_cascade/cascade.py)

## Slide 23 — Pitfalls and checklist
**Timing:** 1:30 (31:45–33:15)
**On slide:**
- Pin model versions (`jev-1.13.0`, not `jev-latest`): thresholds shift between versions
- Calibrate on your own labeled data; calibration is a group property
- `confidence` formulas differ across vendors (Laya vs Jev)
- English first (Jev); text only (Jev) vs text + images (OpenAI)
- Benchmarks are almost all vendor-run; latency claims are 🟡
- Data residency and retention: OpenAI ZDR / HIPAA / US-EU; check every provider
- No free tier found for TypeSafe or OpenAI
- Use Structured Outputs / an LLM when you need generated objects, not decisions

**Speaker notes:**
A checklist before you put one of these in production.

Pin the model version. jev-latest points to 1.13.0 today, but your thresholds are tuned for that version, and a silent upgrade can move them. Calibrate on your own labeled data. Even a few hundred labeled examples tell you more than any vendor chart, and remember calibration is a group property.

Do not assume the confidence field means the same thing everywhere. Unsloth warns that Laya's formula differs from Jev's. Check language and modality: Jev works best in English and is text only; OpenAI also takes images.

Treat benchmarks as vendor claims until someone independent reproduces them. Check data residency and retention per provider; OpenAI documents zero data retention, HIPAA and US or EU residency, others you need to check. Budget for paid keys; I found no free tier. And finally, if you need the model to generate an object or tool arguments, that is not a decision. Use Structured Outputs or function calling, as OpenAI itself recommends.

**Sources:** [TypeSafe: Models](https://docs.typesafe.ai/models.md), [Unsloth: Laya](https://unsloth.ai/docs/models/decision-laya), [OpenAI Decisions guide](https://platform.openai.com/docs/guides/decisions), [research.md §5–6](research.md)

## Slide 24 — Takeaways
**Timing:** 0:45 (33:15–34:00)
**On slide:**
- If code consumes the answer, ask for a decision, not prose
- "System One model" is a real category now: Jev, OpenAI Decisions, Clef, plus open recipes (Unsloth)
- One API shape is emerging: state + typed questions → probabilities + confidence, output free
- It generalizes what we had: classifiers, rerankers, routers, guardrails — now zero-shot
- Cascade it: System 1 first, System 2 and humans for low confidence; measure accuracy and escalation rate on your data

**Speaker notes:**
Five things to remember. If the consumer of an AI answer is code, ask for a decision, not prose. System One models are now a real product category, hosted and open. The API shape is converging on state plus typed questions in, probabilities and confidence out, with output for free. This is a generalization of classifiers, rerankers, routers and guardrails we already had, now zero-shot. And build it as a cascade: System 1 first, System 2 and humans for the uncertain cases, measured on your own data.

## Slide 25 — Questions?
**Timing:** 1:00 (34:00–35:00)
**On slide:**
- Research, comparison, workshop ex1–ex4, this deck and the script
- https://github.com/vusatui/rnd-research/tree/main/system-one-models
- Anton Vusatyi

**Speaker notes:**
Thank you. Everything is in the repo: the research notes with verification markers, the comparison tables, the workshop code you can run with a free OpenRouter key, this deck and the full script. I am happy to take questions, especially about where you would put a System 1 model in your own pipelines.

**Sources:** [README.md](README.md)
