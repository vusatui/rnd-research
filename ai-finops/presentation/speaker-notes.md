# Speaker notes for "Taming the AI bill" (about 30 minutes)

These notes are written to be read aloud, word for word, at a calm pace of roughly 130 words per minute. Each slide has a heading with its number, title and time. Lines in italic brackets are short stage directions and are not spoken. Every claim here comes from the research notes in `../research.md`, the comparison in `../comparison.md`, or from the measured runs in `../workshop/results/`. Numbers that we measured ourselves are always said out loud as ours. They come from free models, priced at published list prices, on sixteen test tickets, so they show a direction and not a guarantee. Prices change every month, and all prices here were read on the nineteenth of October 2026. The questions and answers at the very end are for the discussion and are not part of the 30 minutes.

The timing adds up to thirty minutes. The slides take 1.5, 2, 1, 1, 1.5, 1, 1, 2, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2.5, 1.5, 1.5, 1 and 1 minutes, and slide 20 opens the last two minutes, which belong to questions. The demo is slides 14 and 15, four and a half minutes in total.

---

## Slide 01 · Title · 1.5 min

Hello everyone, and thank you for being here. Today I want to talk about a problem that arrives a few months after an AI feature goes live. The invoice comes, and it is much bigger than anyone expected. People then ask who is spending it, on what, and whether it can be cut without making the product worse.

I will keep this practical and light. You do not need any background in machine learning or in finance. We will start with why the bill surprises people, and then with how the FinOps community suggests looking at AI spend. After that we will go through the levers that we actually tested, which are shorter answers, less context, smaller models, a fast model first, and two kinds of caching. Then we look at gateways and budgets, and at when self-hosting can pay off. In the middle there is a short demo with real output. At the end I will show you where you can try everything yourself. So let's start with the surprise.

## Slide 02 · Cheaper tokens, bigger bills · 2 min

Here is a puzzle. The price of AI keeps falling, and yet the bills keep growing. On the slide, the navy line is the price of getting a fixed level of capability. Epoch AI, which tracks this, measured a fall of roughly thirteen times per year since 2023. That is a very steep decline, and it varies a lot between tasks.

The orange line is the total bill, and this one is a sketch of the argument, not data. The argument is that usage grows faster than prices fall. Agents send the same context again at every step, they retry, and they reason, so one user request can turn into many model calls. Gartner predicts that the inference cost of one agentic workflow will rise by more than five times through 2028, but that is a forecast, not a fact. An Accenture survey found that nine in ten executives say cheaper tokens lead them to build more use cases, and that only one in twenty would simply bank a twenty-five percent price cut. That is a survey, so it is a signal and not proof.

Both things can be true at the same time. The unit price goes down, and the bill goes up. So the conversation has to move from the price of a token to the cost of getting a task done successfully, and we will come back to that.

## Slide 03 · Every step re-sends everything · 1 min

Why does the bill grow faster than the number of users? The slide shows three steps of an agent. A language model has no memory between calls, so at every step the application sends everything again. That means the instructions, the descriptions of the tools, the whole history, and the results of the previous tools. With every step, the stack gets taller, and you pay for the whole stack each time.

On the right you see a second effect. On current flagship price cards, output tokens cost about five times as much as input tokens, and the hidden thinking that reasoning models do is billed as output. So the cost grows with the number of steps multiplied by the size of the context, and not with the number of messages that a user types. This is the main reason why a small pilot can become an expensive production system.

## Slide 04 · Easy-to-miss multipliers · 1 min

On top of that, price lists contain multipliers that are easy to miss. These cards are examples that we read on the vendors' own pages. Long prompts can cross a size tier. One large provider charges double for the input of requests above two hundred seventy-two thousand tokens, and a small model from another provider costs five times more above one hundred thousand. Faster service costs more, since one provider's fast tier is double the standard price and its fastest tier is six times.

Keeping data in a region can add ten percent. And promotions end. One model costs two dollars for input and ten for output per million tokens until the end of November 2026, and double from the first of December. On the bright side, batch and flex tiers give fifty percent off for work that can wait. These prices were read on the nineteenth of October 2026, so check them before you quote them.

## Slide 05 · Cost per task, not per token · 1.5 min

So what should we measure instead? The FinOps Foundation suggests unit costs, such as the cost per inference or per API call, tied to business value. A McKinsey interviewee put it nicely. It is not just about cost per token, it is about cost per task.

We use three numbers for every feature. The first is dollars per task. The second is dollars per successful task, which is the first divided by the pass rate, so that a cheap but wrong setup is punished. The third is dollars per month at your forecast volume. The slide shows the baseline from our own test. Fourteen of sixteen support tickets passed our checks. At the price card of a premium model, two dollars per million input tokens and ten per million output, one ticket cost about one and a quarter cents, and a successful ticket about one point four cents. At a hundred thousand tickets a month, that is around twelve hundred and fifty dollars.

This is our measurement on a small test set, so take the method and not the amounts. Count the tasks that worked, and always say which price card and which date you used.

## Slide 06 · FinOps for AI in three verbs · 1 min

Before the levers, a word on how organizations manage this. The FinOps Foundation says the basic idea still applies, which is that cost equals price times quantity. You lower the price through tiers and commitments, or you lower the quantity, which means fewer tokens. In practice that comes down to three verbs. Measure the spend for each use case. Allocate it to a team and a feature. And limit it with budgets and alerts.

The State of FinOps survey for 2026 had almost twelve hundred respondents, and ninety-eight percent now manage AI spend, compared with thirty-one percent two years earlier. The open billing format called FOCUS is also getting columns for the model, for cached tokens, and for who made the call, but that is still a draft. For now, attribution has to come from your own gateway logs.

## Slide 07 · Our test bench · 1 min

Here is the test bench for the next slides. It is a support feature for a fictional software company. A model answers tickets using a knowledge base of ten sections. We have sixteen tickets, and code checks each answer for the key facts, for forbidden statements, and for the category. There is no model acting as judge, because that adds cost and bias.

Two honest details. First, we used free models, so nothing was ever charged. To make the cost visible, we priced every call at a published list price, which we call the shadow cost. Second, there is one run per configuration and only sixteen tickets, so a difference of one or two tickets is noise. Our checks also have blind spots. A wrong price once passed because the reply also said to contact sales. So the rule for the next slides is to change one lever at a time, and to read cost and quality together.

## Slide 08 · Say less, send less · 2 min

The first two levers are the simplest. The baseline, on the left, sends the whole knowledge base with every ticket and lets the model answer at length. It produced about four hundred output tokens per answer, and fourteen of sixteen tickets passed. Because output costs about five times more than input, the long answers were roughly a third of the total cost.

The second bar asks for a short answer in a small structured format. Output dropped from about four hundred tokens to about eighty-five. Cost fell by twenty-six percent, and quality did not drop. It went from fourteen to fifteen out of sixteen, and the median response time fell from almost nine seconds to about two and a half. The third bar also sends only the three most relevant sections of the knowledge base, instead of all ten. Input tokens went from about forty-two hundred to about fifteen hundred, and the cost fell by sixty-eight percent, still with fifteen out of sixteen passing.

These are our measurements on a premium price card, with a small test set, so the exact percentages will differ for your workload. There is also a risk. If the retrieval step misses the right section, the answer will be wrong. In our test the search found the right section in fourteen of sixteen tickets. So trimming is the biggest lever on a large model, but it needs a test behind it.

## Slide 09 · A smaller model · 1.5 min

The next lever is a smaller model. We used a large and a small free model. On the price card we used, the large one costs about twenty times more than the small one, and on the paid prices of the same two models about nine times. The second card shows that the small model cut the cost by ninety-six percent, with the same fourteen of sixteen tickets passing.

Then comes the surprise on the third card. We combined the small model with the trimmed context, two levers that each worked on their own. The cost fell by ninety-eight percent, but quality collapsed to nine out of sixteen. Trimming suited the large model, which could cope with it, and it hurt the small one, which needed the full text. Levers interact, so each one has to be tested again after you add the next.

And always state which price card and which date you used, because the gap changes with the card. One or two tickets is noise, but nine against fourteen is not.

## Slide 10 · A cascade needs a checker · 1.5 min

A popular idea is a cascade. You send each request to the small model first, and you escalate to the big model only when the answer looks doubtful. The diagram shows the flow, and the whole question is what the check looks like.

Our first check was the one most people try. The small model reports its own confidence, and we escalate below zero point seven five. It escalated only one ticket out of sixteen, and quality fell to thirteen out of sixteen. One ticket asked for the price of the enterprise plan. The knowledge base says only that pricing is custom, but the small model invented a price and reported a confidence of zero point nine five.

So we added a plain code check. Every dollar amount or percentage in the reply must exist in the knowledge base or in the ticket. That caught the invented price, and fourteen of sixteen passed at about ninety-five percent lower cost than the baseline. The escalation signal is the real product. Research on routing reports big savings, but those depend on the benchmark, so measure on your own traffic.

## Slide 11 · Prompt caching · 1.5 min

Prompt caching feels free. If the beginning of your prompt matches a previous request, the provider reuses the work and charges much less for those tokens. The published rules are similar across providers. Reading from the cache costs about a tenth of the normal input price, sometimes less, and writing can cost about a quarter more, though some providers charge nothing for writes.

The catch is that the cache needs an identical start. On the left of the slide, a timestamp and a request number sit at the top, so every request differs from the first token and nothing can be reused. On the right, the same data sits at the end, and the long instructions are identical every time.

We measured this on a prompt of about eight thousand tokens. With the stable start, about sixty-three hundred tokens came from the cache from the second request on. With the dynamic part first, there were none. This was a free endpoint with undocumented caching, and a shorter prompt of about four thousand tokens got no hits. We also simulated the paid rules. A cache written once and never read costs one and a quarter times the normal price, which is worse than none. With a hundred requests in the window, it costs about an eighth. So put stable content first.

## Slide 12 · Similar is not the same · 1.5 min

Semantic caching sounds even better. The system stores answers and returns one when a new question is similar enough. The risk is on the slide. These two questions ask whether single sign-on is available on the business plan, and on the enterprise plan. To an embedding model they are almost the same, and in our test they scored zero point nine five. But the correct answers differ, so the stored answer is wrong for one of them, and it is delivered free and instantly.

This is not only our observation. A 2026 research paper called vCache found that the similarity scores of correct and incorrect cache hits overlap heavily, with averages of zero point eight five and zero point eight four. So no single threshold can guarantee correctness.

We built twenty-four pairs by hand, twelve true paraphrases and twelve near-misses that need a different answer. At a threshold of zero point eight, the cache would have saved eight of twelve paraphrase calls and served nine of twelve wrong answers. The pairs were built to be tricky, so this is a stress test and not a traffic estimate. Use exact-match caching for safe wins, and semantic caching only with validation, short lifetimes, and never for account-specific or numeric answers.

## Slide 13 · One door for every call · 1.5 min

So far we looked at making each call cheaper. The other half is knowing who makes the calls and capping them. The FinOps Foundation points out that the hard part is identifying who used a shared model. The clearest guidance is from AWS, which says to stamp the attribution in a shared client or gateway, and to make it the only route.

We tried this with LiteLLM, which is open source, running on a laptop, with two teams. The support team had a budget of five cents and both models. The growth team had one cent and the small model only. When support kept calling the large model, the gateway stopped it after the budget was crossed, at about a hundred and twelve percent. That is normal, because the check runs before a call, so leave one request of headroom. The growth team was refused when it asked for the large model, so an allow-list is itself a cost control.

Tags on keys were an enterprise feature in this product. We tested only LiteLLM, and the others in the comparison file are documentation only.

## Slide 14 · Live demo: the cost table · 2 min

*[switch to the terminal, in the workshop folder]*

Now for the demo, in two parts. The first needs no key and no network. One command re-scores the saved runs from our workshop, so you see the numbers that I have been quoting. The slide shows a shortened table.

*[run the re-score command]*

Each row is one configuration of the same sixteen tickets. The columns are the name, how many tickets passed our checks, the cost per ticket on a premium price card, and the change against the baseline. The baseline costs a bit more than one cent per ticket and passes fourteen. The concise setup is twenty-six percent cheaper and passes fifteen. Trimming takes it to sixty-eight percent less. The small model is ninety-six percent less, and the small model with trimming is ninety-eight percent less, but look at the pass column. Only nine tickets pass.

That is the point on the right. Cheaper is not always better, and only the two columns together tell the truth. This is a saved run, and a live run may differ slightly, because free models are not deterministic.

## Slide 15 · Live demo: the $0 trap · 2.5 min

For the second part, I want to show a mistake that cost us hours, because it can silently disable every budget you set. We used the gateway from the previous slide. It has a built-in provider for OpenRouter, the service we used to reach the free models. We configured the same model in two ways, and the slide shows both. In the first, the model goes through the generic provider that speaks the common API. In the second, it goes through the built-in OpenRouter provider. In both we set the same custom price, because a free model has no real price.

*[run the two curl requests and read the cost header]*

I send one tiny request to each. On the right you see what the gateway logged. For the first it logged two point eight times ten to the minus six dollars, exactly as expected. For the second it logged zero. Same model, same custom price, different bill.

We traced the cause in the source code of that version. The built-in provider copies the cost that OpenRouter reports in its own response, and that takes precedence over our custom price. For free models OpenRouter reports zero, and a request with zero cost skips the budget checks by design. So the budgets could never trip. The fix is to use the generic provider and put the custom prices on that entry. We have not reported this upstream.

The calculation at the bottom is the lesson. Eighteen input tokens at ten cents per million, plus two output tokens at fifty cents per million, make point zero zero zero zero zero two eight dollars. Check one request against a hand calculation before you trust a budget. On paid OpenRouter models the reported cost is the real bill, which is what you want. The trap bites when you need a different price, such as free models, internal chargeback rates, or a negotiated discount.

## Slide 16 · When does self-hosting pay? · 1.5 min

The last question is whether to run an open model yourself. The answer is about utilization, and the slide shows it on one bar. We built a small calculator where every assumption is visible. A server with eight high-end GPUs at three dollars fifty per GPU hour, always on, plus fifteen thousand dollars a month for operations, comes to about thirty-five thousand dollars a month before it serves a single request. We also assume a throughput of five thousand tokens per second, which is an assumption and not a measurement.

With those assumptions, the server must run at about sixty-four percent average utilization to beat an open model bought through an API. It needs only about eighteen percent to beat a premium price, but that compares two different models, so it counts only if your tests show the open model is good enough. At the higher hyperscaler GPU price, the first case becomes impossible.

The dashed arrow shows a trap. If traffic exists only in business hours, an always-on server is capped at roughly thirty percent average utilization, even if it is saturated all day. Our GPU prices come from secondary sources, and published break-even studies differ by an order of magnitude. Data residency, latency and control are other reasons to self-host, and should be priced separately.

## Slide 17 · Honest limits · 1.5 min

Let me be clear about what this talk does not prove. Our quality numbers come from one pair of free models, on sixteen tickets, with a single run per configuration. A difference of one or two tickets is noise. The shop is a made-up one, so please do not copy our percentages into your business case. Measure your own traffic.

Second, the costs are shadow costs. Free models charged nothing, and we priced every call at a published list price, which moves every month. Third, the caching results are partly simulated. The measured hits come from a free endpoint with undocumented caching, and the savings on paid endpoints were calculated from the published rules. We did not run the batch tiers, prompt compression or model distillation at all. We tested only one gateway, and the others are documentation only. And fourth, many of the surveys I quoted are published by the companies that sell the answers, so I treat them as signals. The FOCUS export that we built has not been checked with the official validator. None of this is a reason to wait. It is a reason to run a small experiment with your own data before you commit to a change.

## Slide 18 · Three takeaways · 1 min

If you remember three things, I hope they are these. First, count the cost per successful task, and not the price per token. A cheap setup that fails is not cheap, and our small model with trimmed context is the example.

Second, change one lever at a time, and re-test quality after each change. Levers interact, and a check is only as good as what it can see, which is true for cascades and for caches alike. And third, put one gateway door in front of every call, so that you know who spent what. Then check the numbers it reports against a hand calculation, because a silent zero can disable every budget you have.

## Slide 19 · Try it yourself · 1 min

If you would like to try this yourself, everything is in a public repository on GitHub. You can see the address on the slide, and you can scan the code with your phone. Open the folder called ai finops.

Inside, you will find the research with its sources, a comparison of the gateways and the price levers, and a workshop of about two and a half hours that uses free models. You can run the workshop, then re-score our runs on your machine, which needs no key at all. The caching simulator, the semantic cache test and the break-even calculator are also offline. Then read the research, and compare the gateways. Only the gateway part needs Docker, and its images are about one and a half gigabytes, so it is better to download them beforehand.

## Slide 20 · Questions · 2 min

That brings me to the end. To sum it up, AI bills grow because usage grows faster than prices fall, and the way to manage that is to measure the cost of successful tasks, to test every lever against quality, and to put a gateway in front of every call. We also saw a silent zero in a cost log, and a cache that serves wrong answers for free.

Thank you very much for listening. I would be happy to take your questions now. If I do not know the answer, I will say so and find out, rather than guess.

*[the rest of the two minutes is open for questions]*

---

## Easy questions you may get

These answers are written the same way, so you can read them aloud if you like.

**1. Will falling token prices fix our budget?**
Not by themselves. Unit prices are falling quickly, but usage grows faster, because agents send more context and make more calls. Both things can be true, so the safe approach is to manage the cost per successful task.

**2. What is the first thing to do?**
Put a shared client or a gateway in front of your model calls and stamp every call with the team and the feature. Then measure the cost per successful task for your most expensive feature, with a small test set that checks quality.

**3. Which lever saves the most?**
It depends on the workload. In our test, trimming the context and using a smaller model saved the most, but the combination hurt quality. So test each lever on your own data, and test again when you combine them.

**4. Is prompt caching risky?**
It is low risk when the start of the prompt is stable. The main danger is a dynamic value at the top, which turns the cache into a paid write that is never read. There is also a privacy angle, and one provider recommends a separate cache key for each customer.

**5. Should we use a semantic cache?**
Only with care. In our stress test, similar questions that need different answers scored as high as true paraphrases. Use exact-match caching first, and keep semantic caching away from account-specific or numeric answers.

**6. Are cascades worth it?**
They can be, if the check that decides on escalation is good. A model's own confidence was not enough in our test, and a simple code check on numbers worked. Research papers report large savings, but those depend on the benchmark.

**7. When should we self-host?**
When you can keep a server busy. Under our assumptions, the break-even was around sixty-four percent utilization against an open model sold through an API. Data residency, latency and control are separate reasons, and you should price them separately.

**8. Do free models make your cost numbers meaningless?**
They make them shadow costs. We priced the tokens at published list prices, so the direction is meaningful but the exact amounts depend on your price card and on the date. Please re-calculate with your own prices.

**9. Which gateway should we pick?**
We tested only LiteLLM, which is open source. The comparison file lists the others, such as Portkey, Cloudflare, OpenRouter, Kong and cloud-native options, with their prices and limits from the documentation. Whatever you choose, verify its cost numbers against a hand calculation.

**10. How do we split the bill between teams?**
Stamp the team and the feature on every call at the gateway, and show the numbers to the teams before you charge them. The open billing format FOCUS is adding the fields for this, but the version with those fields is still a draft.

---

Sources for the facts above are in [`../research.md`](../research.md) and [`../comparison.md`](../comparison.md), and the measured results are in [`../workshop/results/`](../workshop/results/) and [`../workshop-plan.md`](../workshop-plan.md).
