# Speaker notes for "System One models", serious variant (about 26 minutes)

Read aloud at about 130 words per minute. Each heading gives the slide number, title and time. Lines in italic brackets are stage directions and aren't spoken. Facts come from `../../research.md`, the Jev documentation at docs.typesafe.ai, and our own measurement in `../../workshop/METHODOLOGY.md` (150 held-out synthetic support tickets, 2026-11-15). The questions at the end aren't part of the talk time.

The timing adds up to about 26 minutes, including two minutes of questions. Slides 11 to 15 answer why not structured output with a confidence score. The demo is slides 16 to 18. Slides 17 and 18 each play a recorded clip at half speed (no audio) in `present.html`, with timestamped comments to read over it. Press K to pause a clip if you need more time. Slide 21 answers three questions from the rehearsal (the VPS cost is in the Q&A below).

---

## Slide 01 · Title · 1 min

Hi everyone, and thanks for coming. Today I want to show you a kind of AI model that doesn't write text at all. Instead, it makes a decision. These are called System One models, and the one we'll look at closely is called Jev.

Here's the plan. First, what these models are, what a call looks like, and where they fit. Then the question I bet most of you have. Why not just ask a normal language model for structured output with a confidence score? We measured exactly that, on the same set of tickets, and I'll show you the numbers. Then two short recorded demos, and how you can try it yourself. If you've ever called a web API, you already know almost everything you need.

## Slide 02 · Two kinds of AI models · 1.25 min

Most of the AI we use every day is a text generator. You give it text, and it gives you more text back. An answer, a summary, an email, some code. That's the top row. It's what we usually mean when we say a large language model.

Now look at the bottom row. A decision model takes the same kind of input. But what comes out is a decision. It can be a choice between options you defined, a score on a scale, or the chance that the answer to a yes-or-no question is yes. So you get numbers and a pick, not a paragraph.

Why does this matter for developers? When a generator answers in words, your code has to figure out what those words mean. When a decision model answers, your code gets a result it can use right away. There's no free text to parse. So where does the name System One come from?

## Slide 03 · Two ways to think · 1 min

It comes from the psychologist Daniel Kahneman and his book Thinking, Fast and Slow. System one is fast and instinctive. It's you glancing at a message and just knowing it's spam. System two is slow and careful. It's you planning a budget, step by step.

The vendor uses this analogy in its own docs, and I like it. Decision models are built for the quick judgement calls, the System One jobs. They're not here to replace careful reasoning. We'll come back to this idea when we talk about putting a fast model first.

## Slide 04 · What is Jev? · 0.75 min

Jev is a hosted System One model from a company called TypeSafe AI. Hosted means you don't run it yourself. You send a request over the internet, and you get an answer back. Its docs call it the first model of this kind.

There are three facts on the slide. It's one HTTP call. It generates no text. And it returns typed answers, so you get a choice, a score, or a yes-or-no probability. Everything I tell you about Jev comes from the official docs or from my own measurements. It's also available through OpenRouter, and that's how I called it.

## Slide 05 · One call, one decision · 1.25 min

Let's go from left to right. You send Jev two things. The first is the state. That's the text you want it to look at, say a customer message. The second is the questions. For each one, you describe the possible answers in plain words.

Jev reads the text and the questions in one pass. For a question with several options, you get a number for each option, plus the pick and how confident it is. For a yes-or-no question, you get the probability of yes. Here you see a bar for the department and a gauge for urgency.

This drawing is just an illustration. We'll see a real response in a minute. The key point is that every answer has a fixed shape. A choice always comes back as a choice. A yes-or-no question always comes back as a probability. So you write normal code against it, just like any other well-defined API.

## Slide 06 · Three kinds of questions · 0.75 min

There are three kinds of questions. The first is a choice. You list the options, like billing, technical and sales, and you get a probability for each one. The second is a score. You define a scale, say from calm to angry, and the model places the text on it. The third is a yes-or-no question, like whether a message is urgent. You get back the probability of yes. Jev calls this type noul.

You can ask several questions about the same text in one call. And since the options are just plain words in the request, you can change them any time. No retraining needed.

## Slide 07 · Not only Jev · 0.75 min

And Jev isn't the only one. OpenAI has a Decisions API, which was in beta when I looked. Cloudflare released an open-weights decision model called Clef, and it runs on Workers AI. And Unsloth published a recipe for training your own.

So the shape is the same everywhere. You send the text and your questions, and you get typed answers back. Which one is best? Honestly, I don't know. There's no independent comparison yet, and the benchmarks we have come from the vendors. So test on your own data.

## Slide 08 · Where it fits · 0.75 min

Here are six everyday jobs where a decision model fits. Routing, moderation, fraud triage, form checks, intent detection and approvals.

In each of them, a person could decide in a second or two. The problem is, there are way too many items. Where should this message go? Is this comment OK? Does this payment look weird? None of these needs an essay. Each one needs a quick, consistent answer. Let me show you routing in a bit more detail, because that's also the task we measured.

## Slide 09 · Routing · 0.75 min

This one's an illustration. A support ticket comes in. Jev reads it and picks the team. Here it's technical.

The dashed arrow is the interesting part. When the model isn't confident, the ticket goes to a person. And what counts as not confident is decided by your code, not by the model. So the cheap path handles the easy tickets, and your people spend their time on the tricky ones. That leads us to a pattern called fast first.

## Slide 10 · Fast first · 1 min

You put the fast decision model in front. It answers most requests by itself. Only the ones it's not sure about go on to a big language model or to a person. Most requests leave through the top, and just a few take the dashed path down.

How many stay at the first step depends on your data and your threshold. And the rule is simple. Raise the threshold, and the model handles fewer tickets on its own. You get fewer mistakes, but more work for people. Lower it, and more gets automated, but more mistakes slip through. So pick the threshold by comparing what a mistake costs you with what a human review costs you. And now, the question some of you have been waiting to ask.

## Slide 11 · The real alternative · 0.75 min

Why not take a normal language model, ask for structured output, and add a confidence field? That's on the left. A JSON schema with the department and a number, say zero point nine. Modern models follow schemas like that reliably. This is the real competitor to a decision model, and it's a serious one.

On the right is the decision model. On the surface, it gives you the same thing, a label and a number. The difference is where that number comes from.

## Slide 12 · Where the number comes from · 1 min

On the left, the language model writes its confidence. That zero point nine is just a few generated tokens. It's one guess, written after the answer. In our test these numbers were pretty coarse. The models used only twelve to nineteen different values across a hundred and fifty tickets, mostly round ones like zero point nine. And those tokens are output, so you pay for them and you wait for them.

On the right, the decision model computes a probability for every option in one pass. You get the whole picture, not just one number. The vendor says it's trained to be calibrated, and you don't pay for output.

Now, to be fair, a written confidence isn't nonsense. It's just a different kind of number. So the only honest thing to do is measure both. And that's what we did.

## Slide 13 · How we tested · 0.75 min

We built two hundred and fifty realistic support tickets for a made-up software company. Five departments, three levels of urgency. Free models wrote them, and two other models labelled every ticket without seeing each other's answers. When they disagreed, we flagged the ticket as ambiguous.

We kept a hundred and fifty tickets aside as the test set. Jev and four normal chat models saw exactly the same tickets and the same option descriptions. Each chat model was asked for structured output with a confidence field. We measured accuracy, speed and cost per thousand tickets. And we only spent paid budget on the models we were testing.

## Slide 14 · Same 150 tickets · 1.25 min

Here are the results for the department question. Jev got ninety-three percent right. It took about a hundred and sixty milliseconds and cost two and a half cents per thousand tickets. And that's with two questions in one call.

GPT-6 Sol also got ninety-three percent, and its written confidence was just as honest. But it took about two seconds and cost a dollar thirty-four per thousand. Claude Sonnet got ninety-four percent, but it was too modest. When it said fifty-seven percent, it was actually right three times out of four. It took one second and cost two dollars. Claude Haiku got ninety-two percent for ten cents. And the cheap DeepSeek model got ninety-five percent in half a second, for under five cents.

Two quick notes. These accuracy differences are within the noise for a hundred and fifty tickets. And on the harder, more subjective urgency question, Jev was four to eight points behind the chat models.

## Slide 15 · What the numbers say · 0.75 min

So compared with the strong chat models, the decision model was fifty to eighty times cheaper and six to thirteen times faster. And it scored every option in one call. Accuracy and calibration were about the same.

So it wasn't more accurate. If you pick a decision model, pick it for price, speed and format, plus decent probabilities. Don't pick it because you think it's smarter. And whatever you use, measure its confidence on your own data before you put a threshold on it. Now let's see this in code.

## Slide 16 · Demo, the request · 0.5 min

This is a real request, just shortened to fit. The state is a support ticket. It says an API integration has been failing for twenty minutes. Then there are two questions. Which department gets it, out of three teams, and is it urgent, yes or no.

Both clips are recorded. The code is real code from the repo, and the output is real output from Jev through OpenRouter.

## Slide 17 · Demo 1, one call · 4 min

*[timestamped comments: the clip runs 4:04 at half speed; the current line is highlighted in the notes panel while it plays. Space / click pauses]*

- **0:00** — Exercise one. A ticket says our API has been down for twenty minutes. Which team gets it? And do we wake someone up? We need a decision here, not an essay.
- **0:14** — Here's how we designed it. One request carries the ticket and all the questions, and each question lists its options in plain words. Jev gives a probability for every option. Then our code turns those into actions, with its own threshold for each action.
- **0:42** — Why do it this way? One call answers every question. Every option gets a score. And the thresholds live in our code, not in the model.
- **1:00** — Here's the request. It's one POST to the System One endpoint, with a model, a state and the questions.
- **1:12** — We ask two questions in the same request. One is a choice with criteria, and the other is a yes-or-no question about urgency.
- **1:24** — And here the code makes the call. We only route automatically if the probability is at least zero point seven.
- **1:36** — For yes-or-no questions, anything above zero point seven counts as yes, and anything below zero point three counts as no. The gray zone in between gets its own outcome.
- **1:48** — The riskier the action, the higher the bar. To block a comment, we need zero point nine. To approve money, we need zero point nine and a clear yes on policy.
- **2:08** — Now we run it against real Jev. Both questions took about a quarter of a second, and it cost less than two thousandths of a cent.
- **2:26** — The ticket goes to technical with probability one. Urgent comes back at zero point nine nine, so we page the on-call engineer.
- **2:40** — Next, a rude comment. Block comes back at zero point nine two, just over the bar, so it gets blocked.
- **3:02** — Now the expense. It's a forty-two dollar lunch for four, clearly within policy. But approve only comes back at zero point six seven. That's under our bar, so the code sends it to a manager. That's the threshold doing its job.
- **3:24** — So it's the same code and the same thresholds, and we get three different outcomes.
- **3:40** — What are the alternatives? Structured output works too, but you only get one written number, not a probability for every option. Keyword rules are free, but they break easily. Jev scores every option in one call. But it writes no text, and you still need to check its numbers on your own data.

## Slide 18 · Demo 2, same tickets · 2.5 min

*[timestamped comments: the clip runs 2:22 at half speed]*

- **0:00** — Exercise two. Why not just ask a chat model for structured output with a confidence field? Is a decision model really any better? We measured it.
- **0:12** — Here's how we set it up. Same hundred and fifty test tickets, same option descriptions. And two kinds of confidence. Either the chat model writes it, or Jev computes it.
- **0:36** — Every model sees the same options, from one file.
- **0:42** — This is the written confidence. The chat model returns structured output with the label and a confidence field for each question.
- **0:56** — So the model just writes its confidence as a number in the answer.
- **1:06** — And this is the computed confidence. Jev gets one request with both questions, and gives a probability for every option.
- **1:20** — Now we re-score the saved results, and we only show Jev and the written-confidence rows. No API calls here.
- **1:28** — Jev gets ninety-three percent, in a hundred and sixty milliseconds, for two and a half cents per thousand tickets.
- **1:40** — The chat models with written confidence get ninety-two to ninety-five percent. They take half a second to two seconds, and cost from under five cents to two dollars per thousand.
- **1:56** — So here's the summary. Jev is fifty to eighty times cheaper and six to thirteen times faster than the strong models, with the same accuracy within the noise. On urgency it's behind, seventy-eight percent against eighty-two to eighty-six. So it's not more accurate. And that's the end of the demo.

## Slide 19 · Use it, skip it · 0.5 min

So when should you use it? Sorting, yes-or-no checks, high volume, and anything that needs a fast answer. When should you skip it? Writing text, explaining a decision, multi-step reasoning, or open chat. The Jev docs say it plainly. It doesn't write replies, code or explanations. Think of it this way. It tells you whether to open an email, but it won't write the reply.

## Slide 20 · Honest limits · 0.75 min

Now a few honest limits. Jev reads text and images, but not audio or video. English works best, and the docs say other languages are weaker. Test on your own data. Our tickets were synthetic and labelled by language models, which gives chat models a home advantage, and a hundred and fifty tickets is a small sample. And most speed and quality numbers you'll see come from vendors, so treat them as claims. None of this means you should avoid it. It just means you should try it on a small sample first.

## Slide 21 · Your questions · 0.75 min

At the rehearsal, Denis asked some great questions, so here are the short answers.

Can we trust the API? TypeSafe's privacy policy says they don't train on your data. Zero data retention is only for enterprise customers, though. So send only what the decision needs.

Can we host it ourselves? Not Jev. The weights aren't published. But if you need to, there are open options, like Cloudflare's Clef or the Unsloth recipe.

Is it lighter than an LLM? We don't know. The size isn't disclosed.

## Slide 22 · Three takeaways · 0.75 min

If you remember just three things, make it these. One. Pick a decision model because it's cheap, fast and gives you clean, structured answers. In our test it was fifty to eighty times cheaper and up to thirteen times faster than strong chat models. Same accuracy, not better.

Two. The model answers, but your code decides. The thresholds, the routing and the human review are yours to design, and they can be different for every action.

Three. Measure confidence on your own data, whatever you use. Check a few hundred of your own examples, and you'll see which numbers you can actually trust.

## Slide 23 · Try it yourself · 0.5 min

If you want to try it yourself, it's all in the public GitHub repo. Just scan the QR code. It's not super polished, but it's a solid base you can build on. Start with the lite workshop and poke around. And there's also a deeper, more advanced version in there. The whole comparison replays offline, no key needed.

## Slide 24 · Questions · 2 min

So, to wrap up. A System One model doesn't write. It decides. It's a fast, cheap way to make lots of small decisions, with probabilities your code can act on. Just keep your code in charge, and let people handle the unclear cases. And it's not magic. In our test it matched strong chat models on accuracy for a tiny fraction of the cost and time, but it didn't beat them.

Thanks for listening. I'm happy to take your questions. And if I don't know the answer, I'll say so and find out.

*[the rest of the two minutes is open for questions]*

---

## Questions you may get

Written to be read aloud. Numbers are from our test on 150 synthetic tickets; see `../../workshop/METHODOLOGY.md`.

**1. Why not just use structured output with a confidence field?**
You can, and with a strong model it works. GPT-6 Sol was as accurate as Jev, ninety-three percent, and about as well calibrated. The difference was price, speed and format. It cost a dollar thirty-four per thousand tickets, against two and a half cents. It took about two seconds, against a hundred and sixty milliseconds. And it gave one written number instead of a probability for every option.

**2. So is Jev more accurate?**
No, not in our test. On the department question, Jev and the chat models were all within the noise, between ninety-two and ninety-five percent. On the subjective urgency question, Jev was four to eight points behind. So choose it for price, speed and format, not for accuracy.

**3. Are written confidence scores garbage?**
No. In our test the strong models were honest, or even too modest. But the numbers are coarse, only twelve to nineteen different values, and they cost output tokens and time. So measure them before you rely on them.

**4. Did you try other ways to get a confidence?**
Yes, three more, all on the same tickets. First, we read the chat model's own token probabilities for each option, instead of asking it to write a number. With DeepSeek Flash that got ninety-five percent on the department, in under half a second, for under four cents per thousand. But on urgency it was overconfident. When it said ninety-eight percent, it was right only sixty-five percent of the time. Second, we asked DeepSeek five times and counted the votes. That got ninety-seven percent, but it's five calls, fifteen cents per thousand, and only three possible confidence values, so a threshold has almost nothing to work with. Third, a classic word-count classifier trained on our hundred training tickets. It's free and instant, but it only got seventy-two percent on the department and fifty-three on urgency. None of this changes the conclusion.

**5. How fast and how cheap is it, really?**
The docs list four point two cents per million input tokens, and output is free. In our test, through OpenRouter, a request with two questions took about a hundred and sixty milliseconds in the typical case, and cost about two and a half cents per thousand tickets.

**6. How did you test, and can I trust a synthetic dataset?**
We used two hundred and fifty synthetic tickets, two blind labellers, and a hundred and fifty held out for testing, with the same options for every model. The weak spot is that the labels come from language models, which favours chat models. And a hundred and fifty tickets is small. That's why I report the noise, and why I keep telling you to test on your own data.

**7. Could we host such a model ourselves?**
Not Jev. It's a hosted service. The docs say the same weights serve every account, and TypeSafe hasn't published them. But there are open options. Cloudflare released Clef, with twenty-seven billion parameters, and Clef-flash, with nine billion, under the Apache 2.0 license, using the same System One request format. Unsloth publishes a recipe to turn a small open model into a decision model, for example Qwen 3.5 with under a billion parameters, on a four gigabyte GPU. And there's the classic route. You can fine-tune a small encoder like ModernBERT, with about a hundred and fifty million parameters, on your own labels. Or you can run an open eight billion parameter chat model and read its token probabilities yourself. As a quick free check, we took a thirty-three million parameter embedding model with logistic regression and trained it on our hundred training tickets. It got eighty-three percent on the same test set, in about eleven milliseconds per ticket on four CPU cores. Jev got ninety-three with no training at all. I haven't tested Clef locally, so I don't know how it does on our tickets.

**8. Does it explain its answer?**
No. It gives you the decision and the probabilities, but no reasoning. If you need to know why, send those cases to a language model.

**9. Does it work in other languages, or with images?**
The docs say English works best. It also reads images. Test both before you rely on them.

**10. Safety: why should I trust the Jev API?**
Trust it as far as the documents go, and check the rest. The privacy policy says TypeSafe won't train or fine-tune any model on your input, and that the service is hosted in the US. Zero data retention is offered to enterprise customers. Otherwise, data is kept as long as reasonably necessary, and they don't give an exact period. The trust center lists a SOC 2 Type Two report for 2026, available on request. It also lists subprocessors in the US. AWS stores and processes live request data, and the GPU providers Modal, Nebius and CoreWeave process prompts without storing them. For EU data, the data processing agreement relies on the standard contractual clauses. If you go through OpenRouter, that's a second company in the path. OpenRouter says it doesn't store prompts unless you opt in. It keeps request metadata, screens for abuse material, and lets you require zero data retention per request or for the whole account. I couldn't find the data policy label for the TypeSafe endpoint on OpenRouter, so check that Jev is still available with zero retention turned on. In practice, send only the fields the decision needs, pseudonymize names and IDs, keep a fallback rule or a human queue for when the API is down, pin the model version, and measure it on your own data.

**11. Is it free to try?**
As far as I could find, new TypeSafe accounts don't get free credits. With an OpenRouter key, the first exercise costs a fraction of a cent, and the whole comparison replays offline with no key at all.

**12. Is it lighter than a large language model?**
We don't know its size. TypeSafe doesn't publish Jev's parameter count or architecture, and OpenRouter lists its quantization as unknown. What we can tell you is what we measured. On our tickets, one call with two questions took about a hundred and sixty milliseconds in the typical case, and cost two and a half cents per thousand tickets. The strong chat models took one to two seconds and cost a dollar thirty-four to two dollars per thousand. The small DeepSeek model took half a second and about five cents. So it's cheaper and faster to use. But whether the model itself is smaller isn't disclosed.

**13. How much would it cost to host such a model on a VPS?**
These are Hetzner list prices, checked on November sixteenth, in euros per month without VAT. The rest is my estimate. A small encoder classifier runs fine on a CPU server. A shared four-core server with eight gigabytes starts at thirty euros a month, and a dedicated two-core one at thirty-seven. An eight billion parameter open model needs a GPU. Hetzner's GEX45 server, with a twenty-four gigabyte card, costs two hundred and fourteen euros a month, plus a two hundred and nine euro setup fee. My estimate is that an eight billion model fits on that card, but I haven't benchmarked it. For scale, at Jev's measured price, a million tickets a month costs about twenty-five dollars. So self-hosting only pays off on price at very high volume. The usual reasons to do it are data control and latency. And remember, you also pay with your own time for operations, monitoring and updates.

---

Sources: [`../../research.md`](../../research.md), [`../../workshop/METHODOLOGY.md`](../../workshop/METHODOLOGY.md), the [Jev documentation](https://docs.typesafe.ai/concepts/system-one), the [Jev models page](https://docs.typesafe.ai/models.md).

Sources for questions 7, 10, 12 and 13 (checked 2026-11-16): [Jev models page](https://docs.typesafe.ai/models.md) (same weights for every account, no size published, data handling), [TypeSafe legal](https://docs.typesafe.ai/legal.md), [Privacy Policy](https://typesafe.ai/legal/privacy-policy) (updated 2025-11-19), [Data Processing Addendum](https://typesafe.ai/legal/data-processing) (updated 2026-04-24), [Trust Center](https://trust.typesafe.ai/) and [subprocessors](https://trust.typesafe.ai/subprocessors), [OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection), [OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr), [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [OpenRouter Jev endpoint](https://openrouter.ai/api/v1/models/typesafe/jev-1.14/endpoints), [Cloudflare Clef changelog](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/), [Unsloth decision-model guide](https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth), [ModernBERT-base](https://huggingface.co/answerdotai/ModernBERT-base), [Hetzner Cloud regular performance](https://www.hetzner.com/cloud/regular-performance), [Hetzner Cloud general purpose](https://www.hetzner.com/cloud/general-purpose), [Hetzner GEX45](https://www.hetzner.com/dedicated-rootserver/gex45/), local CPU benchmark [`demo/runs/cpu-bench.txt`](demo/runs/cpu-bench.txt).
