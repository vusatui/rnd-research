# Speaker notes: "System One" for everyone (~30 min)

Deck: `presentation.excalidraw` (18 frames, one per slide; open at excalidraw.com, see `README.md`). **Slides have almost no text on purpose: everything you say is here.** Tone: relaxed, funny, short sentences. If something is not covered here, say "good question, I will check" instead of guessing.

Timing: 1 + 1.5 + 2.5 + 2 + 2.5 + 1 + 1 + 1.5 + 1 + 1 + 1 + 1 + 2 + 5 + 1.5 + 1.5 + 1 + 2 = **30 min** (demo 5 min, questions 2 min at the end plus any you take on the way).

---

### Slide 01: Title (1 min)
"Today: a new kind of AI model with a boring name and a fun idea: **System One**. No math, no deep dive. By the end you will know what it is, when to use it, and you will see me call one."

### Slide 02: The hook, overkill (1.5 min)
Ask the room: "Is this email urgent?" Everybody can answer that in one second. Now picture asking a chatbot: you often get *three paragraphs* of polite explanation, and then your code has to dig the answer out of the text. "We only needed YES or NO." That gap is what today is about.

### Slide 03: Two ways to think (2.5 min)
There is a famous idea from the psychologist Daniel Kahneman (book: *Thinking, Fast and Slow*): our brain has two modes. **System 1**: fast, gut feeling, no effort ("is that dog friendly?"). **System 2**: slow, careful ("plan a trip budget"). Both are useful; the trick is not to use the slow one for everything. The name "System One" for these models comes from this idea (TypeSafe's docs say so).

### Slide 04: Two kinds of AI models (2 min)
Most AI you have used is a **writer**: text in, text out (ChatGPT-style LLMs). The new family is a **decider**: text in, a *decision* out: a choice, a score, a yes/no probability. No sentences. Think "multiple choice test" versus "essay question".

### Slide 05: One call, one decision (2.5 min)
Walk left to right. You send two things: the **text** (the customer message) and the **question with options** ("which team: billing, tech or sales?"). The model answers with **numbers for each option**, e.g. "billing: very likely". The bar chart is an *illustration*, not real output. Key line: **no essay, just numbers**, so your code can act on it directly with no text parsing.

### Slide 06: Meet Jev (1 min)
Jev is made by a company called TypeSafe AI and is described in its own docs as the first "System One" model. It is a hosted API. Do **not** quote launch dates, funding or speed numbers from random websites (many unofficial Jev sites exist; only docs.typesafe.ai is trusted).

### Slide 07: Same idea, many names (1 min)
Jev is not alone. OpenAI has a Decisions API (public beta at the time of research), Cloudflare released an open-weights model called Clef, and the Unsloth team published a recipe for training your own decision model. Different logos, same shape of API: text and questions in, typed answers out. If someone asks which is best: "no independent comparison exists yet; test on your own data".

### Slide 08: Three kinds of questions (1.5 min)
1. **Pick one**: choose among options you define (tech/billing/sales). The docs call it *Choice*.
2. **Rate it**: put it on a scale you define, e.g. calm / annoyed / angry. *Score*.
3. **Yes or no**: the probability of "yes". *Noul* (Jev's name for it).
You can ask several questions about the same text in one call.

### Slide 09: Where it shines (1 min)
Six everyday jobs: ticket routing, moderation, fraud triage, form checks, intent detection, approvals. "Whenever a human would glance and decide in a second."

### Slide 10: Ticket routing (1 min)
"App crashes at checkout" goes to the tech team. A sorting robot, basically. The example is illustrative. Mention: if the model is unsure, send to a human.

### Slide 11: Moderation (1 min)
Three comments, three actions: block, allow, ask a human. The third one is the important idea: the model also tells you *how sure it is*, so borderline cases go to people.

### Slide 12: Fraud triage (1 min)
A $9,999 payment at 3 a.m. abroad: take a closer look; a $4 coffee: fine. It is not a final verdict, it is a very fast first look. Illustrative example.

### Slide 13: Fast first, big brain if unsure (2 min)
The cost story. The fast model answers the easy majority *(do not quote a number; it depends on your data)*; the unsure ones go to a big LLM, which is slower and pricier. "Cheap bouncer at the door, expensive specialist inside." The relay-race picture: Zap runs, passes the baton to the Professor only when needed.

### Slide 14: LIVE DEMO (5 min)
Open `workshop-lite/` (see its README). Steps:
1. Show the request: just `state` and `questions` (30 s). Point at `criteria`: those are our options.
2. Run `python jev_client.py ticket`; show the answer: choice, probabilities, confidence (1 min).
3. Run `comment` and talk about the "review" bucket (1 min).
4. Show that the *code* decides what to do with the answer (the last printed line) (1 min).
5. Optional: `bash curl_example.sh`: "it is just HTTP" (30 s).
**Be honest about the backend:** if you have no Jev key, the demo runs on the local emulator (a free LLM wearing a Jev costume; the response says `EMULATOR`). Say so out loud: "same request shape as real Jev, different engine behind it". If you have a key, set `JEV_BASE_URL`/`JEV_API_KEY` and say it is the real thing. LLM-based outputs can differ between runs; have the saved `workshop-lite/sample_output.txt` as a backup.

### Slide 15: Use it / skip it (1.5 min)
Use it for sorting, yes/no checks, huge volume and speed. Not for writing, chatting, explaining *why* (Jev's docs say it does not write replies, code or explanations), or hard multi-step reasoning. "Jev will never write your email. It will tell you whether to open it."

### Slide 16: Honest caveats (1.5 min)
- Text first: Jev reads text (no audio/video); image input exists only behind an experimental "danger zone" header in the docs, so treat it as not ready.
- English works best; other languages are weaker (documented).
- Always test on **your** data; probabilities are only trustworthy if you check them.
- Most speed/quality numbers come from the vendors themselves, so treat them as claims, not proof.

### Slide 17: Remember 3 things (1 min)
1. Pick the right brain for the job (fast vs slow).
2. The model answers, **your code decides**.
3. Fast first, big LLM only if unsure.

### Slide 18: Questions (2 min + overflow)
Thank people; invite questions; offer the repo link.

---

## Easy questions you may get

1. **Is it just a classifier?** Close cousin. Old classifiers needed training data for every new task. A System One model is meant to work "zero-shot": you describe the options in plain words in the request.
2. **Why not just ask ChatGPT for a one-word answer?** You can, and for small volumes it is fine. Decision models aim to be faster and cheaper, return numbers for every option (and a confidence), and do not need output parsing.
3. **How fast / how cheap is it?** Jev's docs list a price of $0.042 per million input tokens with free output (docs.typesafe.ai/models). Speed numbers on the web come mostly from vendors or unofficial sites; measure it yourself.
4. **Can I run it on my own servers?** Jev is hosted. Open-weights options exist (e.g. Cloudflare's Clef) and the Unsloth recipe lets you train your own; quality differs, so test.
5. **Can I trust the percentages?** They are designed to be calibrated (Jev's docs say so) but that is a claim about groups of answers, not a guarantee for each one. Check on your own labeled examples.
6. **Does it explain its answer?** No. It returns the decision and the probabilities, not reasoning text. If you need the "why", use an LLM for those cases.
7. **Does it work in other languages?** Docs say English is best and other languages are handled less well; test before relying on it.
8. **What about private data?** The Jev docs state that it is not trained on customer requests and mention zero-data-retention for enterprise customers; read the legal page and ask your security team before sending real customer data.
9. **Do I need a GPU or ML skills?** No. It is one HTTP call with JSON.
10. **Is it free to try?** Per third-party trackers, new Jev accounts currently get no free credits (verify in the console). The workshop uses a free emulator so everyone can follow along.

Sources for every claim above: [`../research.md`](../research.md) (verified / vendor / unofficial markers), [Jev docs](https://docs.typesafe.ai/concepts/system-one), [Jev models page](https://docs.typesafe.ai/models.md).
