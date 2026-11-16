# Speaker notes for "System One models", serious variant (about 27 minutes)

Read aloud, word for word, at about 130 words per minute. Each heading gives the slide number, title and time; lines in italic brackets are stage directions and are not spoken. Facts come from `../../research.md`, the Jev documentation at docs.typesafe.ai, and our own measurement in `../../workshop/METHODOLOGY.md` (150 held-out synthetic support tickets, eight methods, 2026-11-15). The questions at the end are not part of the talk time.

The timing adds up to about 27 minutes, including two minutes of questions. Slides 11 to 15 answer why not structured output with a confidence score. The demo is slides 16 to 18: slide 16 sets it up, and slides 17 and 18 each play a recorded clip at half speed (no audio) in `present.html`, with timestamped comments to read over it. Press K to pause a clip if you need more time.

---

## Slide 01 · Title · 1 min

Hello everyone, and thank you for being here. Today I want to talk about a kind of AI model that does not write text at all. It makes a decision. These are called System One models, and the one we will look at closely is called Jev.

First, I will explain what these models are, what a call looks like, and where they fit. Then I will answer the question I expect from most of you: why not simply ask a normal language model for structured output with a confidence score? We measured exactly that on the same set of tickets, and I will show you the numbers. Then two short recorded demos, and where you can try it yourself. If you have ever called a web API, you already know almost everything you need.

## Slide 02 · Two kinds of AI models · 1.25 min

Most of the AI we use every day is a text generator. You give it text, and it gives you more text back: an answer, a summary, an email or some code. That is the top row, and it is what we usually mean by a large language model.

A decision model, in the bottom row, takes the same kind of input, but what comes out is a decision. It can be a choice among options you defined, a score on a scale, or the probability that the answer to a yes or no question is yes. The result is a set of numbers and a pick, not a paragraph.

For developers this matters. When a generator answers with words, your program has to work out what they mean. When a decision model answers, your program gets a result it can use directly, with no free text to parse. So where does the name System One come from?

## Slide 03 · Two ways to think · 1 min

It comes from the psychologist Daniel Kahneman and his book Thinking, Fast and Slow. System one is fast and instinctive, like glancing at a message and knowing it is spam. System two is slow and deliberate, like planning a budget step by step.

The vendor's documentation uses this analogy, and I find it helpful. Decision models are built for the quick judgement calls, the System One jobs, not to replace careful reasoning. We will come back to this when we talk about using a fast model first.

## Slide 04 · What is Jev? · 0.75 min

Jev is a hosted System One model from a company called TypeSafe AI. Hosted means you do not run it yourself: you send a request over the internet and get an answer back. Its documentation describes it as the first model of this kind.

Three facts are on the slide. It is one HTTP call, it generates no text, and it returns typed answers: a choice, a score or a yes or no probability. Everything I say about Jev comes from the official documentation or from my own measurements. It is also available through OpenRouter, which is how I called it.

## Slide 05 · One call, one decision · 1.25 min

From left to right. You send Jev two things. The state, which is the text you want it to look at, for example a customer message. And the questions, where you describe the possible answers in plain words.

Jev reads the text and the questions in one pass. For a question with several options, you get a number for each option, plus the pick and how confident it is. For a yes or no question, you get the probability of yes. Here that is a bar for the department and a gauge for urgency.

This drawing is an illustration; we will see a real response shortly. The point is that every answer has a fixed shape. A choice always comes back as a choice, and a yes or no question as a probability, so you write ordinary code against it, like any well-defined web interface.

## Slide 06 · Three kinds of questions · 0.75 min

There are three kinds of questions. A choice: you list options, such as billing, technical and sales, and get a probability for each. A score: you define an ordered scale, for example from calm to angry, and the model places the text on it. And a yes or no question, such as whether a message is urgent, which returns the probability of yes. Jev calls this type noul.

You can ask several questions about the same text in one call, and because the options are plain words in the request, you can change them at any time without retraining.

## Slide 07 · Not only Jev · 0.75 min

The same idea exists elsewhere. OpenAI has a Decisions API, in beta when I looked. Cloudflare released an open-weights decision model called Clef, which runs on Workers AI. And Unsloth has published a recipe for training your own.

The shape is similar: text and questions in, typed answers out. Which one is best, I do not know, because there is no independent comparison yet, and the existing benchmarks come from the vendors. So test on your own data.

## Slide 08 · Where it fits · 0.75 min

Six everyday jobs where a decision model fits: routing, moderation, fraud triage, form checks, intent detection and approvals.

In each, a person could decide in a second or two, but there are far too many items. Where should this message go? Is this comment acceptable? Does this payment look unusual? None of these needs an essay, each needs a quick, consistent answer. Let me show routing in more detail, because it is also the task we measured.

## Slide 09 · Routing · 0.75 min

This is an illustration. A support ticket arrives, Jev reads it and picks the team, here technical.

The dashed arrow is the interesting part. When the model is not confident, the ticket goes to a person, and what counts as not confident is decided by your code, not by the model. The cheap path handles the easy tickets, and your staff spend their time on the unclear ones. That leads to a pattern called fast first.

## Slide 10 · Fast first · 1.25 min

Put the fast decision model in front. It answers most requests by itself, and only the ones it is not sure about go on to a big language model or a person. Most requests leave through the top, a few take the dashed path down.

How many stay at the first step depends on your data and your threshold. In our own test, with the threshold at zero point nine five, Jev handled three quarters of the tickets on its own, with no wrong automated answers in the test set. If a mistake costs five dollars and a human review fifty cents, that comes to about a hundred and twenty-seven dollars per thousand tickets, against three hundred and thirty-three for automating everything and five hundred for sending everything to people. It is one small synthetic test, not a promise, but it shows the trade-off. The fast model plays quick instinct, the big model or the person plays careful thought. Now, the question some of you have been waiting to ask.

## Slide 11 · The real alternative · 0.75 min

Why not take a normal language model, ask for structured output, and add a confidence field? That is on the left: a JSON schema with the department and a number, say zero point nine. Modern models follow such schemas reliably. This is the real competitor to a decision model, and a serious one.

On the right, the decision model gives the same thing on the surface, a label and a number. The difference is where the number comes from.

## Slide 12 · Where the number comes from · 1 min

On the left, the language model writes its confidence. Zero point nine is a few generated tokens, one guess written after the answer. In our test these numbers were coarse: only twelve to nineteen different values across a hundred and fifty tickets, mostly round ones like zero point nine. And those tokens are output, which you pay for and wait for.

On the right, the decision model computes a probability for every option in one pass. You get the whole distribution, the vendor says it is trained to be calibrated, and output is not billed.

To be fair, a written confidence is not nonsense. It is a different kind of number, not a useless one, so the only honest thing is to measure both. So we did.

## Slide 13 · How we tested · 0.75 min

We built two hundred and fifty realistic support tickets for a made-up software company, with five departments and three levels of urgency. Free models wrote them, and two other models labelled each ticket blindly. Where they disagreed, the ticket was flagged as ambiguous.

A hundred and fifty tickets were held out as the test set. Eight methods saw exactly the same tickets and option descriptions: Jev, strong and small chat models with written confidence, token probabilities, voting, and a classic classifier. We measured accuracy, calibration, latency and cost per thousand tickets. The paid budget went only to the models under test.

## Slide 14 · Same 150 tickets · 1.25 min

These are the results for the department question. Jev: ninety-three percent correct, a small calibration error of zero point zero four, about a hundred and sixty milliseconds, and two and a half cents per thousand tickets, for one call with two questions.

GPT-6 Sol with structured output got the same ninety-three percent and the same calibration error, but took about two seconds and cost a dollar thirty-four per thousand. Claude Sonnet got ninety-four percent, but its confidence was too modest: when it said fifty-seven percent, it was right three times out of four. It took one second and cost two dollars.

The cheap DeepSeek model reached ninety-five percent in half a second for under five cents. Five votes reached ninety-seven, but with only three possible confidence values, a very blunt knob for a threshold.

Two remarks. These accuracy differences are within the noise of a hundred and fifty tickets. And on the more subjective urgency question, Jev was four to nine points behind the chat models.

## Slide 15 · What the numbers say · 0.75 min

Compared with strong chat models, the decision model was fifty to eighty times cheaper and six to thirteen times faster, and it scored every option in one call. Accuracy and calibration were about the same.

So it was not more accurate. Choose a decision model for price, speed and format, plus decent probabilities, not because you expect it to be smarter. And whatever you use, measure its confidence on your own data before you put a threshold on it. Now let me show this in code.

## Slide 16 · Demo, the request · 0.5 min

This is a real request, shortened to fit. The state is a support ticket saying an API integration has been failing for twenty minutes. The questions are the department, a choice between three teams, and whether it is urgent, a yes or no question.

The two clips are recorded, with real code from the repository and real output from Jev through OpenRouter.

## Slide 17 · Demo 1, one call · 4 min

*[timestamped comments: the clip runs 4:04 at half speed; the current line is highlighted in the notes panel while it plays. Space / click pauses]*

- **0:00** — Exercise one. A ticket says our API has been failing for twenty minutes. Which team gets it, and do we wake someone up? We need a decision, not an essay.
- **0:14** — The design: one request carries the ticket and all the questions, each with options in plain words. Jev returns a probability for every option, and our code turns them into actions, with a threshold per action.
- **0:42** — Why: one call answers all questions, every option is scored, and the thresholds live in our code.
- **1:00** — The request: one POST to the System One endpoint with a model, a state and the questions.
- **1:12** — Two questions in one request: a choice with criteria, and a yes-or-no question for urgency.
- **1:24** — Here the code decides: route automatically only if the probability is at least zero point seven.
- **1:36** — For yes-or-no: yes above zero point seven, no below zero point three, and the band in between gets its own outcome.
- **1:48** — Risk sets the bar. Blocking a comment needs zero point nine, and approving money needs zero point nine plus a clear yes on policy.
- **2:08** — Now the run against real Jev. Both questions took about a quarter of a second and cost less than two thousandths of a cent.
- **2:26** — The ticket goes to technical with probability one, urgent at zero point nine nine, so on-call is paged.
- **2:40** — The rude comment: block at zero point nine two, just above the bar, so it is blocked.
- **3:02** — The expense, a forty-two dollar lunch for four, clearly within policy, gets approve at only zero point six seven. Below our bar, so the code escalates it to a manager. The threshold doing its job.
- **3:24** — Same code, same thresholds, three different outcomes.
- **3:40** — Alternatives. Structured output works too, but gives one written number, not a distribution. Keyword rules are free but brittle. Jev scores every option in one call, but writes no text, and its numbers still need checking on your data.

## Slide 18 · Demo 2, same tickets · 3.5 min

*[timestamped comments: the clip runs 3:34 at half speed]*

- **0:00** — Exercise two: why not ask a chat model for structured output with a confidence field? Can we trust that number? We measured it.
- **0:12** — The design: the same hundred and fifty held-out tickets, the same option descriptions, five ways to get a confidence, one evaluation script.
- **0:38** — All methods live in one file and see the same options.
- **0:44** — Method A, structured output: a label plus a confidence field per question, and the prompt asks the model to be calibrated.
- **1:08** — Method B reads the model's token probabilities for each option.
- **1:20** — Method C asks five times at temperature one and counts the votes.
- **1:30** — And Jev: one request with both questions, a probability for every option.
- **1:44** — We run the evaluation on the saved results, with no API calls.
- **1:52** — One row per method: accuracy, calibration error, how much we can automate, distinct confidence values, latency and cost.
- **2:10** — Jev: ninety-three percent, calibration error zero point zero four, a hundred and sixty milliseconds, two and a half cents per thousand.
- **2:20** — The strong chat models: ninety-three to ninety-four percent, one to two seconds, one thirty-four to two dollars per thousand.
- **2:30** — Now the harder, subjective question: urgency.
- **2:38** — Token probabilities say zero point nine eight, and are right only sixty-five percent of the time. That is overconfidence.
- **2:50** — Side by side: token probabilities are overconfident, while GPT-6 Sol's written confidence lines up well. Measure first, then trust.
- **3:10** — The summary: Jev is fifty to eighty times cheaper and six to thirteen times faster than the strong models, with the same accuracy within the confidence intervals. Not more accurate. That is the end of the demo.

## Slide 19 · Use it, skip it · 0.5 min

A decision model fits sorting, yes or no checks, high volumes and fast answers. It does not fit writing text, explaining its decision, multi-step reasoning or open conversation; the Jev documentation says plainly that it does not write replies, code or explanations. In short, it tells you whether to open an email, but it will not write the reply.

## Slide 20 · Honest limits · 0.75 min

Four limits. Jev reads text and images, but no audio or video. English works best; the documentation says other languages are handled less well. Test on your own data: our tickets were synthetic and labelled by language models, which favours chat models, and a hundred and fifty is a small sample. And most speed and quality numbers you will read come from vendors, so treat them as claims. None of this is a reason to avoid the technology, only to try it on a small sample first.

## Slide 21 · Three takeaways · 0.75 min

Three things to remember. First, pick a decision model for price, speed and format. In our test it was fifty to eighty times cheaper and up to thirteen times faster than strong chat models, at the same accuracy, not better.

Second, the model answers, and your code decides. Thresholds, routing and human review are yours to design, per action.

Third, measure confidence on your own data, whatever the method. A reliability table on a few hundred of your own examples tells you which numbers you can trust.

## Slide 22 · Try it yourself · 0.5 min

Everything is in a public GitHub repository; scan the code or use the address, and look for the folder system-one-models. You will find the research notes, the workshop with three exercises, the dataset, all saved results and a methodology note. The comparison replays offline with one command, without any key, and with an OpenRouter key the same client talks to real Jev for a fraction of a cent.

## Slide 23 · Questions · 2 min

To sum up: a System One model does not write, it decides. It is a fast and cheap way to make many small decisions with probabilities your code can act on, as long as your code stays in charge and people handle the unclear cases. In our test it matched strong chat models on accuracy at a tiny fraction of the cost and time, but it did not beat them.

Thank you for listening. I am happy to take your questions, and if I do not know an answer, I will say so and find out.

*[the rest of the two minutes is open for questions]*

---

## Questions you may get

Written to be read aloud. Numbers are from our test on 150 synthetic tickets; see `../../workshop/METHODOLOGY.md`.

**1. Why not just use structured output with a confidence field?**
You can, and with a strong model it works. GPT-6 Sol was as accurate as Jev, ninety-three percent, and about as well calibrated. The differences were price, speed and format: a dollar thirty-four per thousand tickets against two and a half cents, about two seconds against a hundred and sixty milliseconds, and one written number instead of a probability for every option.

**2. So is Jev more accurate?**
No, not in our test. On the department question all model-based methods were within the noise of each other, between ninety-two and ninety-seven percent. On the subjective urgency question Jev was four to nine points behind the chat models. Choose it for price, speed and format, not accuracy.

**3. Are written confidence scores garbage?**
No. In our test the strong models were honest or even too modest. But they are coarse, twelve to nineteen distinct values, and they cost output tokens and time. Measure them before you use them.

**4. Why not use logprobs or ask several times?**
Both were accurate. But token probabilities were overconfident on the subjective question: when they said ninety-eight percent, they were right sixty-five percent of the time. Voting five times costs five calls and gives only a few possible values, so a threshold has very few positions.

**5. How fast and how cheap is it, really?**
The documentation lists four point two cents per million input tokens, output free. In our test, through OpenRouter, a request with two questions took about a hundred and sixty milliseconds in the middle case and cost about two and a half cents per thousand tickets.

**6. How did you test, and can I trust a synthetic dataset?**
Two hundred and fifty synthetic tickets, two blind labellers, a hundred and fifty held out, the same options for every method. The weak spot is that the labels come from language models, which favours chat models, and a hundred and fifty tickets is small. That is why I report intervals and tell you to test on your own data.

**7. Could we host such a model ourselves?**
Not Jev. It is a hosted service: the documentation says the same weights serve every account, and TypeSafe has not published the weights. But there are open options. Cloudflare released Clef, twenty-seven billion parameters, and Clef-flash, nine billion, under the Apache 2.0 license, with the same System One request format. Unsloth publishes a recipe to turn a small open model, such as Qwen 3.5 with under a billion parameters, into a decision model on a four gigabyte GPU. And there is the classic route: a small encoder like ModernBERT, with about a hundred and fifty million parameters, fine-tuned on your labels, or an open eight billion parameter chat model where you read the token probabilities yourself. As a quick free check, a thirty-three million parameter embedding model with logistic regression, trained on our hundred training tickets, got eighty-three percent on the same test set in about eleven milliseconds per ticket on four CPU cores. Jev got ninety-three without any training. I have not tested Clef locally, so its quality on our tickets is unknown.

**8. Does it explain its answer?**
No. It returns the decision and the probabilities, but no reasoning. If you need to know why, pass those cases to a language model.

**9. Does it work in other languages, or with images?**
The documentation says English works best. It also reads images. Test both before you rely on them.

**10. Safety: why should I trust the Jev API?**
Trust it as far as the documents go, and verify the rest. The privacy policy says TypeSafe will not train or fine-tune any model on your input, and that the service is hosted in the United States. Zero data retention is offered to enterprise customers; otherwise data is kept as long as reasonably necessary, and the retention period is not specified. The trust center lists a SOC 2 Type II report for 2026, available on request, and subprocessors in the US: AWS stores and processes live request data, and the GPU providers Modal, Nebius and CoreWeave process prompts without storing them. For EU data, the data processing agreement relies on the standard contractual clauses. If you go through OpenRouter, there is a second company in the path. OpenRouter says it does not store prompts unless you opt in, keeps request metadata, screens for abuse material, and lets you require zero data retention per request or for the whole account. I could not find the data policy label of the TypeSafe endpoint on OpenRouter, so check that Jev is still available with zero retention enforced. In practice: send only the fields the decision needs, pseudonymize names and identifiers, keep a fallback rule or a human queue for when the API is down, pin the model version, and measure it on your own data.

**11. Is it free to try?**
As far as I could find, new TypeSafe accounts get no free credits. With an OpenRouter key, the first exercise costs a fraction of a cent, and the whole comparison replays offline without any key.

**12. Is it lighter than a large language model?**
We do not know its size. TypeSafe does not publish the parameter count or the architecture of Jev, and OpenRouter lists its quantization as unknown. What we can say is what we measured. On our tickets, one call with two questions took about a hundred and sixty milliseconds in the middle case and cost two and a half cents per thousand tickets. The strong chat models took one to two seconds and cost one thirty-four to two dollars per thousand. The small DeepSeek model took half a second and about five cents. So it is cheaper and faster to use, but whether the model itself is smaller is not disclosed.

**13. How much would it cost to host such a model on a VPS?**
These are list prices from Hetzner, checked today, in euros per month without VAT, and the rest is an estimate. A small encoder classifier runs fine on a CPU server: a shared four core server with eight gigabytes costs from thirty euros a month, and a dedicated two core one from thirty-seven. An eight billion parameter open model needs a GPU: Hetzner's GEX45 server with a twenty-four gigabyte card costs two hundred and fourteen euros a month plus a two hundred and nine euro setup fee. My estimate is that an eight billion model fits on that card, but I have not benchmarked it. For scale, at Jev's measured price a million tickets a month cost about twenty-five dollars. So self-hosting pays off on price only at very high volume; the usual reasons are data control and latency, and you also pay with your own time for operations, monitoring and updates.

---

Sources: [`../../research.md`](../../research.md), [`../../workshop/METHODOLOGY.md`](../../workshop/METHODOLOGY.md), the [Jev documentation](https://docs.typesafe.ai/concepts/system-one), the [Jev models page](https://docs.typesafe.ai/models.md).

Sources for questions 7, 10, 12 and 13 (checked 2026-11-16): [Jev models page](https://docs.typesafe.ai/models.md) (same weights for every account, no size published, data handling), [TypeSafe legal](https://docs.typesafe.ai/legal.md), [Privacy Policy](https://typesafe.ai/legal/privacy-policy) (updated 2025-11-19), [Data Processing Addendum](https://typesafe.ai/legal/data-processing) (updated 2026-04-24), [Trust Center](https://trust.typesafe.ai/) and [subprocessors](https://trust.typesafe.ai/subprocessors), [OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection), [OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr), [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [OpenRouter Jev endpoint](https://openrouter.ai/api/v1/models/typesafe/jev-1.14/endpoints), [Cloudflare Clef changelog](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/), [Unsloth decision-model guide](https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth), [ModernBERT-base](https://huggingface.co/answerdotai/ModernBERT-base), [Hetzner Cloud regular performance](https://www.hetzner.com/cloud/regular-performance), [Hetzner Cloud general purpose](https://www.hetzner.com/cloud/general-purpose), [Hetzner GEX45](https://www.hetzner.com/dedicated-rootserver/gex45/), local CPU benchmark [`demo/runs/cpu-bench.txt`](demo/runs/cpu-bench.txt).
