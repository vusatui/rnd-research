# Speaker notes for "System One models", serious variant (about 32 minutes)

These notes are written to be read aloud, word for word, at a calm pace of roughly 130 words per minute. Each slide has a heading with its number, title and time. Lines in italic brackets are short stage directions and are not spoken. Facts come from the research notes in `../../research.md`, the Jev documentation at docs.typesafe.ai, and our own measurement, described in `../../workshop/METHODOLOGY.md` (150 held-out synthetic support tickets, eight methods, 2026-11-15). The questions and answers at the very end are for the discussion and are not part of the talk time.

The timing adds up to about 32 minutes, including two minutes of questions. Slides 11 to 15 are the new section on why not structured output with a confidence score. The demo is slides 16 to 19: slide 16 sets it up, and slides 17 to 19 each play a short recorded clip (no audio) in `present.html` while you read the notes over it. Press K to pause a clip if you need more time.

---

## Slide 01 · Title · 1.5 min

Hello everyone, and thank you for being here. Today I want to talk about a kind of AI model that does not write text at all. Instead, it makes a decision. These models are called System One models, and the one we will look at closely is called Jev.

Here is the plan for the next half hour. First, I will explain what these models are and how they differ from the chatbots we already know. Then we will look at what a single call to one of them looks like, and where such a model fits into real work. After that, I will answer the question I expect from most of you: why not simply ask a normal language model for structured output with a confidence score? We measured exactly that, on the same set of tickets, and I will show you the real numbers. Then three short recorded demos, and at the end, where you can try all of this yourself.

You do not need any machine learning background. If you have ever called a web API, you already know almost everything you need. So let's start with the basic idea.

## Slide 02 · Two kinds of AI models · 1.75 min

Most of the AI we use every day is a text generator. You give it some text, and it gives you more text back. That could be an answer, a summary, an email draft, or a piece of code. This is what the top row of the slide shows, and it is what we usually mean when we say a large language model.

Now look at the bottom row. A decision model starts with the same kind of input, some text. But what comes out is not more text. What comes out is a decision. It might be a choice among a few options that you defined yourself, a score on a scale, or the probability that the answer to a yes or no question is yes. On the slide this is drawn as a small bar chart and a check mark, because the result is a set of numbers and a pick, not a paragraph.

I think this difference matters a lot for developers. When a generator answers with words, your program has to read those words and work out what they mean. When a decision model answers, your program receives a result it can use directly. There is no free text to parse, and no guessing whether the model said yes or maybe.

That is the whole idea of the talk in one sentence. So where does the strange name System One come from? Let's look at that next.

## Slide 03 · Two ways to think · 1.25 min

The name comes from a well-known idea by the psychologist Daniel Kahneman, who described it in his book Thinking, Fast and Slow. He said that people have two modes of thinking. System one is fast and instinctive. It is what you use when you glance at a message and just know it is spam. System two is slow and deliberate. It is what you use when you plan a budget or work through a hard problem step by step.

The vendor's own documentation uses this analogy for these models, and I find it helpful. The point is on the bottom of the slide. Decision models are built for the quick judgement calls, the System One kind of jobs. They are not meant to replace careful reasoning. We can build software the same way, and we will come back to this idea when we talk about using a fast model first.

Now that we have the idea, let me introduce the specific model we will use today.

## Slide 04 · What is Jev? · 1.25 min

Jev is a hosted System One model from a company called TypeSafe AI. Hosted simply means that you do not run it yourself. You send a request over the internet, and you get an answer back. Its own documentation describes it as the first model of this kind.

The slide shows three simple facts about Jev. First, it is one HTTP call. Second, it generates no text. Third, it returns typed answers, which means a choice, a score or a yes or no probability, rather than sentences.

One small warning before we continue. If you search the internet for Jev, you will find many unofficial websites with launch dates, funding figures and speed numbers. I have not been able to verify those, so I will not quote them today. Everything I say about Jev comes from the official documentation, or from measurements I made myself for this talk. Jev is also available through OpenRouter, which is how I called it.

With that in place, let's look at what a call actually looks like.

## Slide 05 · One call, one decision · 2 min

Let's walk through this picture from left to right. On the left, you send two things to Jev. The first is the state. That is simply the text you want it to look at, for example a message from a customer. The second is the list of questions. These are the things you want to know about that text, and you describe the possible answers in plain words.

In the middle is Jev itself. It reads the text and the questions in one pass. On the right is what comes back. For a question with several options, you get a number for each option, and the model also tells you which one it picked and how confident it is. For a yes or no question, you get the probability of yes. On the slide this is drawn as a bar for the department and a gauge for urgency.

Please note that this drawing is an illustration, not real output. We will see a real response in a few minutes. The important thing to remember is that the answer is numbers, not sentences. Your code can act on those numbers right away. You ask the questions you care about, and the model replies with a typed answer for each of them. Typed here means that every answer has a clear shape. A choice always comes back as a choice, and a yes or no question always comes back as a probability. Because of that, you can write ordinary code against it, in the same way you would write code against any other well-defined web interface.

Let's look more closely at the kinds of questions you can ask.

## Slide 06 · Three kinds of questions · 1.25 min

There are three kinds of questions, and they cover a surprising amount of everyday work. The first is a choice. You give a list of options, such as billing, technical and sales, and the model picks one and tells you how likely each option is.

The second is a score. Here you define an ordered scale, for example from calm to angry, and the model places the text somewhere on it.

The third is a yes or no question, such as whether a message is urgent. The answer is the probability of yes. In the Jev interface this type is called noul, which is a slightly odd name, but you only need to remember that it means yes or no.

You can ask several questions about the same text in a single call. And because you describe the options in plain words in the request, you can change them at any time, without retraining anything. Jev is not the only product that works this way, so let's take a quick look around.

## Slide 07 · Not only Jev · 1 min

The same idea exists elsewhere. OpenAI has a Decisions API, which was in beta when I looked into this. Cloudflare has released a decision model called Clef, with open weights, which you can use on its Workers AI platform. And the team at Unsloth has published a recipe for training your own decision model.

These are different vendors, but the shape is similar. You send text and questions in, and you get typed answers back. If you ask me which one is best, my honest answer is that I do not know, because there is no independent comparison yet. The benchmark numbers that exist come from the vendors themselves, so the right approach is to test on your own data. So where would you use a model like this?

## Slide 08 · Where it fits · 1.25 min

Here are six everyday jobs where a decision model fits well. Routing, moderation, fraud triage, form checks, intent detection, and approvals.

What these have in common is that a person could look at each item and decide in a second or two, but there are far too many items for a person to handle them all. That is exactly the gap a fast decision model can fill. Think about the work behind a busy online shop, a large community forum or a payment system. In each of them, there is a constant stream of small questions. Where should this message go? Is this comment acceptable? Does this payment look unusual? None of these questions needs an essay. Each of them needs a quick and consistent answer, and that is the sweet spot for a decision model. Let me show one of them, routing, in a little more detail, because it is also the task we measured.

## Slide 09 · Routing · 1 min

The first example is routing. Please keep in mind that this is an illustration I made up to explain the idea. Imagine a support ticket arrives. Jev reads it and picks the right team, and in this case the technical team gets it.

The dashed arrow at the bottom is the part I find most interesting. When the model is not confident about its answer, the ticket does not go to a team at random. It goes to a person. And the threshold for what counts as not confident is a decision made by your code, not by the model. This way the fast and cheap path handles the easy tickets, and your support staff spend their time on the ones that are genuinely unclear. This idea of sending only the unclear cases somewhere else leads straight to a pattern called fast first.

## Slide 10 · Fast first · 1.75 min

A common pattern is to put the fast decision model in front. It answers most of the requests by itself, quickly and cheaply. Only the requests it is not sure about are passed on, to a big language model or to a person. You can see this on the slide. Most requests leave through the top, and only a few take the dashed path down.

How many stay at the first step depends entirely on your data and on the threshold you choose, so I will not quote a vendor number. But I can tell you what we saw in our own test, which I will describe in a moment. On our support tickets, with the threshold at zero point nine five, Jev handled three quarters of the tickets on its own, and none of those automated answers was wrong in the test set. The other quarter went to a person. That is one small synthetic test, not a promise, but it shows the shape of the trade-off.

This also brings us back to the two ways of thinking from earlier. The fast model plays the part of quick instinct, and the big model or the person plays the part of careful thought. And now let me answer the question that I am sure some of you have been waiting to ask.

## Slide 11 · The real alternative · 1 min

The question is this. Why not just take a normal language model, ask it for structured output, and add a confidence field? You can see that on the left. A JSON schema with the department and a number, say zero point nine. Modern models follow such a schema reliably, so nobody parses free text any more. This is the real competitor to a decision model, and it is a serious one.

On the right is the decision model. Same input, and also a label and a number. So on the surface both give you the same thing. The difference is not in the format. The difference is in where the number comes from, and that is the next slide.

## Slide 12 · Where the number comes from · 1.75 min

On the left, the language model writes its confidence. The number zero point nine is a few tokens that the model generates, the same way it generates any other word. It is one guess, written after the answer. In practice these written numbers are coarse. In our test, the models used only twelve to nineteen different values across a hundred and fifty tickets, mostly round numbers like zero point nine or zero point nine five. And those tokens are output, which you pay for and wait for.

On the right, the decision model computes a probability for every option in a single pass. Nothing is written. You get the whole distribution, not just one number, and the vendor says the model is trained to make those probabilities calibrated. Output is not billed.

Now, I want to be fair here. Research shows that written confidence from chat models is not nonsense. A 2023 study by Tian and colleagues found that for chat models it is often better calibrated than their raw token probabilities. Another study, by Xiong and colleagues, found that it tends to be overconfident, and that this gets better with stronger models. So it is a different kind of number, not a useless one. The only honest thing to do is to measure both. So we did.

## Slide 13 · How we tested · 1 min

Here is how. We built two hundred and fifty realistic support tickets for a made-up software company, with five departments and three levels of urgency. Free models wrote them, and two other models labelled every ticket blindly, without seeing each other's answers. Where the two labellers disagreed, we flagged the ticket as ambiguous.

We kept one hundred and fifty tickets aside as a test set. Every method saw exactly the same tickets and exactly the same descriptions of the options. Eight methods in total: Jev, strong and small chat models with written confidence, token probabilities, voting, and an old-school classifier. For each, we measured accuracy, calibration, latency and the cost per thousand tickets. One lesson from building this: use free models to make the data, and spend the paid budget only on the models you are testing.

## Slide 14 · Same 150 tickets · 1.75 min

These are the results for the department question. The top row is Jev. Ninety-three percent correct, a calibration error of zero point zero four, which is small, about a hundred and sixty milliseconds per ticket, and two and a half cents per thousand tickets. That is one call, with two questions in it.

The next two rows are strong chat models with structured output. GPT-6 Sol got the same ninety-three percent, with the same calibration error. Its written confidence was honest. But it took about two seconds, and it cost a dollar thirty-four per thousand tickets. Claude Sonnet got ninety-four percent, and its confidence was too modest: when it said fifty-seven percent, it was right three times out of four. It took one second and cost two dollars per thousand.

The cheap DeepSeek model was even a little more accurate, ninety-five percent, in half a second, for under five cents. Asking it five times and counting votes reached ninety-seven percent, but then the confidence has only three possible values, so it is a very blunt knob for a threshold.

Two honest remarks. First, the accuracy differences in this table are within the statistical noise of a hundred and fifty tickets. Second, on the harder, more subjective question of urgency, Jev was less accurate than the chat models, by four to nine points.

## Slide 15 · What the numbers say · 1 min

So what do the numbers say? Compared with strong chat models, the decision model was fifty to eighty times cheaper, and six to thirteen times faster. It answered both questions in one call and scored every option, so your code gets a full distribution to set thresholds on. Its accuracy and calibration were about the same as the strong models on the main question.

And here is the line I want you to take home. It was not more accurate. If you choose a decision model, choose it for price, speed and format, plus decent probabilities. Do not choose it because you expect it to be smarter. And whatever you use, a decision model or written confidence from a chat model, measure that confidence on your own data before you put a threshold on it.

Now let me show you how this looks in code.

## Slide 16 · Demo, the request · 1 min

This is what a real request looks like, shortened to fit the screen. It has two parts. The state, which is the text to judge, here a support ticket saying that an API integration has been returning errors for twenty minutes. And the questions: the department, a choice between three teams, and whether the message is urgent, a yes or no question.

The demos you will see are recorded, so we do not depend on the network here, and everything in them is real code from the repository and real output. This time the requests go to the real Jev, through OpenRouter. There are three short clips, one for each exercise of the workshop.

## Slide 17 · Demo 1, one call · 2 min

*[the clip starts by itself; press K to pause it, R to restart it]*

Exercise one. The problem: one ticket, several things to decide, and the code should be in charge. The design is simple. One request carries all the questions. The model returns a probability for each answer, and our code turns those probabilities into actions, with a different threshold for each action.

Here is the request in the client, and here is the line where the code decides. A yes or no answer counts as yes above zero point seven and as no below zero point three, and everything in between gets its own outcome. Risky actions need more: blocking a comment or approving an expense needs at least zero point nine.

Now we run it against real Jev. The ticket goes to the technical team, with a probability of one, and urgent at zero point nine nine, so the on-call engineer is paged. That took about a quarter of a second, both questions in one request, and cost less than two thousandths of a cent. The rude comment comes back as block with zero point nine two, just above the bar, so it is blocked. And the expense, a forty-two dollar lunch for four people, which is clearly within policy, comes back as approve with only zero point six seven. That is below our zero point nine bar, so the code escalates it to a manager. This is the threshold doing its job. A structured output call could do the routing too, but it would need one generated answer per question, and it would give us one written number instead of a distribution.

## Slide 18 · Demo 2, same tickets · 1.75 min

*[the clip starts by itself]*

Exercise two is the comparison you just saw on the slides, as code. The problem: decide how to get a trustworthy confidence. The design is one dataset, one evaluation script, and five ways of getting a confidence, each in a small function in the same file.

Here is the structured output method. The schema has the department, the urgency, and a confidence field for each, and the prompt asks the model to be calibrated. Here is the token probability method, which reads the model's own probabilities for the first token of each option. Here is the voting method, five samples at temperature one. And here is Jev, one request with both questions. All of them get exactly the same option descriptions.

Now we run the evaluation. It reads the saved results and prints one table: accuracy, calibration error, how much we could automate at ninety-five percent accuracy, the number of distinct confidence values, latency, and cost. And here are the reliability tables, confidence on the left and how often the model was right on the right. Look at the token probabilities on the urgency question. When they say ninety-eight percent, they are right only sixty-five percent of the time. That is overconfidence, and it is exactly what would hurt you if you put a threshold on it. The written confidence from GPT-6 Sol, by contrast, lines up well. Measure first, then trust.

## Slide 19 · Demo 3, the threshold · 1.25 min

*[the clip starts by itself]*

Exercise three answers the last practical question: where should the threshold be? The design is a small simulation. Every wrong automatic answer costs five dollars, every human review costs fifty cents, and we sweep the threshold from zero to one.

Here is the result for Jev. Automating everything costs three hundred and thirty-three dollars per thousand tickets, because of the mistakes. Sending everything to people costs five hundred. The cheapest point is a threshold of zero point nine five: three quarters automated, no mistakes in the test, a hundred and twenty-seven dollars. And at the bottom, the same optimum for every method. The strong chat models land at a hundred and thirty-five to a hundred and thirty-eight dollars, close to Jev. At this volume, the model's own price is tiny compared to mistakes and reviews. Its price and speed start to matter at large volume and when you need an answer in milliseconds. That is the end of the demo.

## Slide 20 · Use it, skip it · 0.75 min

So when is a decision model the right tool? It fits sorting things into groups, yes or no checks, high volumes, and situations where you need fast answers.

It is not the right tool for writing text, for explaining why it decided something, for reasoning that takes many steps, or for open conversation. The Jev documentation says plainly that it does not write replies, code or explanations. For those jobs, a large language model is the better choice. A simple way to remember it: the decision model tells you whether to open an email, but it will not write the reply.

## Slide 21 · Honest limits · 1 min

Four limits. First, these models read text, and Jev also reads images, but there is no audio or video.

Second, English works best. The documentation says other languages are handled less well, so test carefully if your data is in another language.

Third, test on your own data. Our own measurement used synthetic tickets labelled by language models, which gives chat models a home advantage, and a hundred and fifty tickets is a small sample. Your numbers will be different.

And fourth, most of the speed and quality numbers you will read come from the vendors, so treat them as claims, not proof. None of these limits is a reason to avoid the technology. They are reasons to try it on a small sample first.

## Slide 22 · Three takeaways · 1 min

If you remember only three things, I hope they are these. First, pick a decision model for price, speed and format. In our test it was fifty to eighty times cheaper and up to thirteen times faster than strong chat models, at the same accuracy, but not better.

Second, the model answers, and your code decides. The thresholds, the routing and the human review are yours to design, and they can differ for every action.

And third, measure confidence on your own data, whatever method you use. Written confidence from a chat model can be good, and computed probabilities can be off. A reliability table on a few hundred of your own examples will tell you which one you can trust.

## Slide 23 · Try it yourself · 0.75 min

Everything is in a public repository on GitHub. You can see the address on the slide, or scan the code with your phone. Look for the folder called system-one-models.

There you will find the research notes with their sources, the workshop with its three exercises, the dataset, all saved results, and a methodology note that explains exactly how we tested. The whole comparison replays offline with one command, without any key. If you have an OpenRouter key, the same client talks to real Jev, and a run of the first exercise costs a fraction of a cent.

## Slide 24 · Questions · 2 min

That brings me to the end. A System One model does not write, it decides. It is a fast and cheap way to make many small decisions with probabilities your code can act on, as long as your code stays in charge and people handle the unclear cases. And it is not magic: in our test it matched strong chat models on accuracy at a tiny fraction of the cost and time, but it did not beat them.

Thank you very much for listening. I would be happy to take your questions now. If I do not know the answer, I will say so and find out, rather than guess.

*[the rest of the two minutes is open for questions]*

---

## Questions you may get

These answers are written the same way, so you can read them aloud if you like. Numbers are from our test on 150 synthetic tickets; see `../../workshop/METHODOLOGY.md`.

**1. Why not just use structured output with a confidence field?**
You can, and with a strong model it works. In our test GPT-6 Sol was as accurate as Jev, ninety-three percent, and its written confidence was about as well calibrated. The differences were price, speed and format: it cost a dollar thirty-four per thousand tickets against two and a half cents, it took about two seconds against a hundred and sixty milliseconds, and it gave one written number instead of a probability for every option.

**2. So is Jev more accurate?**
No, not in our test. On the department question all the model-based methods were within the statistical noise of each other, between ninety-two and ninety-seven percent. On the subjective urgency question Jev was four to nine points behind the chat models. Choose it for price, speed and format, not for accuracy.

**3. Are written confidence scores garbage?**
No. The research says they are often better calibrated than a chat model's token probabilities, and in our test the strong models were honest or even too modest. But they are coarse, twelve to nineteen distinct values in our test, and they cost output tokens and time. Measure them before you use them.

**4. Why not use logprobs or ask several times?**
Both work, and both were accurate. But token probabilities were overconfident on the subjective question: when they said ninety-eight percent, they were right sixty-five percent of the time. Voting five times costs five calls and gives only a few possible values, so a threshold has very few positions.

**5. How fast and how cheap is it, really?**
The documentation lists four point two cents per million input tokens, output free. In our test, through OpenRouter, a request with two questions took about a hundred and sixty milliseconds in the middle case and cost about two and a half cents per thousand tickets.

**6. How did you test, and can I trust a synthetic dataset?**
Two hundred and fifty synthetic tickets, two blind labellers, a hundred and fifty held out, the same options for every method. The weak spot is that the labels come from language models, which favours chat models, and a hundred and fifty tickets is small. That is why I report intervals and why I tell you to test on your own data.

**7. Can I run it on my own servers?**
Jev itself is hosted. Open-weights options exist, for example Cloudflare's Clef, and the Unsloth recipe lets you train your own. Quality differs, so test before you decide.

**8. Does it explain its answer?**
No. It returns the decision and the probabilities, but no reasoning. If you need to know why, pass those cases to a language model.

**9. Does it work in other languages, or with images?**
The documentation says English works best. It also reads images. Test both before you rely on them.

**10. What about private data?**
The documentation states that it is not trained on customer requests, and it mentions zero data retention for enterprise customers. Still read the legal page and talk to your security team before sending real data.

**11. Is it free to try?**
New TypeSafe accounts currently get no free credits, as far as I could find. Through an OpenRouter key with credits, the first exercise costs a fraction of a cent, and the whole comparison replays offline without any key.

---

Sources: [`../../research.md`](../../research.md), [`../../workshop/METHODOLOGY.md`](../../workshop/METHODOLOGY.md), the [Jev documentation](https://docs.typesafe.ai/concepts/system-one), the [Jev models page](https://docs.typesafe.ai/models.md), Tian et al. 2023 ([arXiv:2305.14975](https://arxiv.org/abs/2305.14975)), Xiong et al. 2024 ([arXiv:2306.13063](https://arxiv.org/abs/2306.13063)).
