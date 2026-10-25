# Speaker notes for "AI and legacy code" (about 30 minutes)

These notes are written to be read aloud, word for word, at a calm pace of roughly 130 words per minute. Each slide has a heading with its number, title and time. Lines in italic brackets are short stage directions and are not spoken. Every claim here comes from the research notes in `../research.md`, the comparison in `../comparison.md`, the workshop results in `../workshop-plan.md`, and the code in `../workshop/`. Sources were checked on October 17, 2026. Our own measurements are called out as ours, vendor statements are called out as claims, and anything we could not verify is said out loud. The questions and answers at the very end are for the discussion and are not part of the 30 minutes.

The timing adds up to thirty minutes. Slides 1 to 20 take 1, 1.5, 1.5, 1, 1.5, 1.5, 1.5, 2, 1.5, 2, then 1.5 each for slides 11 to 14, 2 for slide 15, 1.5 for slides 16 and 17, then 1, 1 and 2. The demo is slides 11 and 12, three minutes in total. Slide 20 opens the last two minutes, which belong to questions.

---

## Slide 01 · AI and legacy code · 1 min

Hello everyone, and thank you for being here. Today I want to talk about old software, the kind that runs banks, insurers and governments, and about what artificial intelligence can and cannot do for it. Much of that software is written in COBOL and runs on mainframes.

The title says it in one line. Translating old code into new code is getting easy. Proving that the new code does the same thing as the old code is the real job. I will explain why, show a real experiment that we ran on an open source mainframe program, and then give you a short map of what the big vendors offer. You do not need to know COBOL. I will explain everything we need along the way.

## Slide 02 · Translation is getting cheap · 1.5 min

Let me start with two headlines from this year. On February 23, Anthropic published an article saying that its coding tool can automate the exploration and analysis of COBOL systems, so that modernization takes quarters instead of years. That is a vendor talking about its own product, so I mark it as a claim. The next day, IBM's share price fell by more than thirteen percent. I only know that from a news site quoting Reuters, so I treat it as secondary information. IBM's answer was that translation captures almost none of the real complexity.

Three weeks later, on March 17, AWS announced that code transformation in its mainframe modernization service is now offered at no cost. Before, it was priced per line of code. That one I read on the AWS page myself.

So here is the question for the rest of the talk. If translating the code costs nothing, what are people actually going to pay for? My short answer is two things. Understanding what the old system really does, and proving that the new one does the same.

## Slide 03 · A program is not the system · 1.5 min

What does legacy actually mean in practice? Our test subject is AWS CardDemo, an open source credit card application published by AWS under the Apache license. The program we modernize is called CBACT04C. It is the monthly interest calculation job, 652 lines of COBOL.

But the program is not the system. On the slide you see a picture made by our own dependency graph tool. A job control script runs the program. The program reads three data files, updates the account file, and writes a file of transactions. It pulls in five copybooks, which are shared definitions of the data layouts, and it calls a system service to stop with an error code. Every one of those connections is a place where a rewrite can go wrong.

For the whole CardDemo tree, the tool found 157 nodes and 385 connections in under a second. That is our own measurement. It also showed that other batch programs touch the account file, so you cannot change it in isolation, and that sixteen online programs jump to a program whose name sits in a variable. A static tool cannot resolve those. Real systems add screens, databases and schedulers on top. The lesson is to do discovery with a parser, and to let the model explain the result, not invent it.

## Slide 04 · Few know the dependencies · 1 min

Is this a real problem for real organizations? A report from Kyndryl, published on October 1, 2026, asked two thousand technology leaders in twelve industries. Only nine percent said that they fully understand the dependencies between their applications. Nearly half said their modernization is behind schedule.

Please note that this is a survey by a services company, so it reflects what that company sees. But it fits what we found in our own small experiment. It also fits an analyst report from ISG in April, which said that organizations use generative AI to extract and validate business rules, and prove that the new system behaves the same by running both in parallel. Understanding and proving. Those two words will come back.

## Slide 05 · Two schools · 1.5 min

Let me give you the quick landscape. There are four classic strategies. Keep the code and move it to a new platform. Convert it mechanically. Rewrite it in a new, idiomatic style. Or buy a package and retire the code. For the middle two, there are two technical schools.

The first school uses rule-based converters. Examples are Heirloom, the refactor path of AWS Transform, which used to be called Blu Age, and several specialists. They produce code that you can trust to behave the same way, but it often reads like COBOL written in Java. Heirloom's own phrase is that it compiles and does not translate.

The second school uses language model pipelines. Examples are the reimagine path of AWS Transform, Google's Mainframe Assessment Tool, IBM's Bob for Z, open source agents from Microsoft, and Mechanical Orchard. They give you modern code, and then you must prove it is right.

The interesting part is that the two schools are converging. Everybody now combines a model with deterministic analysis and with an oracle, which means something that can say what correct means. In our case, the oracle is the old system, running.

## Slide 06 · Better readers than writers · 1.5 min

Where is the model actually good? The best recent evidence that I found is a paper called COBOL-Coder, from Concordia University and FPT, published this year. On 143 small programs, translating COBOL into Java works very well. GPT-4o compiled 97 percent of the results, and 85 percent passed the tests. Now turn it around. Java into COBOL. GPT-4o compiled only 4 percent, and about 2 percent passed.

So the models read COBOL far better than they write it. That is what the slide shows. But please read the small print at the bottom of the slide. These tasks were single files, without shared definitions, without job control, and without calls to other programs. The authors also note that practitioners see model output as junior developer drafts, and that restartability and error handling are requirements that no benchmark covers.

Microsoft's own developer blog is honest about this too. It says its early attempts with GPT-4 gave a good mix of educated guesses and hallucinational gibberish. So the model is good at explaining code, at analysis on top of a real graph, at extracting rules with citations, at writing tests, and at writing small pieces from a precise specification. Remember that last point.

## Slide 07 · Where it breaks · 1.5 min

Now to the heart of the talk. Business rules are the part that everybody talks about. The interest formula, the fee, the eligibility check. Models are decent at those. The failures live below the business rules.

I have four examples on the slide. How a negative number is stored, where the sign is hidden inside the last digit. Whether a calculation rounds or truncates. What a keyed file does that a plain file does not. And the error codes that operators and schedulers react to.

Mechanical Orchard published an experiment on this in June, also on CardDemo. Their field chief technology officer had a model write a Java copy of a CardDemo program. It compiled and it ran. But it treated a keyed file as a flat file, wrote negative numbers as text with a minus sign, dropped one branch, and replaced error code 999 with exit code 12. Each of those would break a downstream job or an operator's runbook. Mechanical Orchard sells verification, so this is their own experiment and we did not reproduce it. But on the next slides you will see that we hit the same kind of problem ourselves.

## Slide 08 · One missing word · 2 min

Here is our first example, and it is a small one. This is the actual interest line from the COBOL program. It takes a balance, multiplies it by the annual rate in percent, and divides by twelve hundred, which is twelve months times one hundred. What matters is a word that is not there. The word is ROUNDED. Without it, COBOL cuts off the extra digits and never rounds up. Our hand-written reference version does the same in Python, using a round-down setting.

Now look at the boxes on the right. They show real output from our test harness. A free model wrote a candidate from the COBOL source alone, without any list of rules. It did what most programmers would do with money and rounded to the nearest cent. The old program computed 12 dollars and 49 cents. The candidate computed 12 dollars and 50 cents. In another case, 99 cents became one dollar.

One cent sounds harmless. But it is one cent on every transaction, every month, on every account, and the totals will no longer agree with the ledger. And none of our rule extraction runs, which you will see in a few minutes, listed truncation as a rule. The model had read the code and had still missed the behaviour. This is also why the harness matters so much. A person reviewing the candidate would see a sensible rounding call and move on, because rounding is exactly what we expect in code that handles money.

## Slide 09 · The forgotten last account · 1.5 min

The second example is my favourite, because it is a real defect in the sample code that nobody had to plant.

The program loops over its input until the end of the file. Inside the loop, when the account number changes, it posts the previous account's interest to the balance. There is also a branch meant to post the last account at the end of the file. It reads perfectly. But the loop checks its condition first, so when the end of the file is reached the loop exits, and that branch never runs. The result is that the last account gets its interest transactions written, but its balance is never updated.

We found this by running the program, not by reading it. When we ran our reference version with the defect fixed, it matched the old system in only 9 of our 25 scenarios. So what should you do? In a real bank, some process may have grown around this behaviour, such as a manual correction or a reconciliation report. Copying the bug or fixing it is not an engineering decision. It is a business decision, and it should be made explicitly, with the differences in hand. A model that helpfully fixes it has taken that decision without asking.

## Slide 10 · The diamond · 2 min

Now to the pattern that ties everything together. Mechanical Orchard calls it the diamond. You feed exactly the same input to two things. One is the running old system, which is your oracle. The other is the new code. Then you compare the outputs, field by field, with a rule per field that says what equivalence means. In our harness, timestamps are masked, filler bytes are ignored, and a strict mode compares every byte.

To get the old program running, we took CardDemo at a fixed version and compiled the program unchanged with the open source GnuCOBOL. Keyed files are emulated with indexed files, and two mainframe services are replaced with small stand-ins. The build takes about a second and one run takes about 20 milliseconds.

Our harness has 25 scenarios. They cover the sample data, edge amounts, a single account, twenty generated portfolios and two error paths. Both sides for all 25 take about half a second.

Building it taught us a few things before any model was involved. The error code 999 shows up on Linux as exit status 231, so an operator watching for 999 would see nothing. A text field keeps binary zeros where you would expect spaces. The sample data has all balances at zero, so it proves nothing. And our own web service first returned money as floating point numbers.

The big vendors sell productized diamonds. Google's Dual Run runs both systems side by side and compares. Mechanical Orchard's tool verifies against captured production data. IBM generates tests for equivalence.

## Slide 11 · Live demo: the reference · 1.5 min

Now to the demo. We start with the reference, which is the Python version that we wrote by hand from verified rules. The command is on the slide. It runs the diamond, so for each scenario it runs the real COBOL program and the Python version on the same input, and compares them.

The output shows one line per scenario, with the name, whether the old program finished normally or stopped with an error, and the verdict. The first lines are the sample data and the edge amounts. Near the end are two scenarios where the old program is expected to stop with error code 999, for example when an account does not exist. Both sides must stop in the same way, and they do. The last line says that all 25 scenarios are equivalent, in half a second.

I have shortened the output on the slide, and it comes from a clean clone run on October 17. Running it live needs GnuCOBOL on the machine, so I will either run it here or show this recorded output. What I want you to see is how cheap this check is. Half a second means you can run it on every change.

*[run the diamond command, or stay on the recorded output]*

## Slide 12 · Live demo: a wrong candidate · 1.5 min

Now the same harness, but with a different candidate. This one was written by a free model that received only the COBOL source. The command on the slide uses the implementation option to point the diamond at the model's file.

The harness reports the differences field by field. In the first transaction, the old system wrote 12.49 and the candidate wrote 12.50. In another one, 0.99 against 1.00. And in the last lines, you see something worse. For one account, the old program leaves the balance at 560 while the candidate adds 12.5 million of interest to it. That is the last account defect from before. The candidate rounded, and it also posted the last account.

I have simplified the lines for the slide, and they come from a recorded run. The scores of the three candidates that were written from COBOL alone were 1, 3 and 2 out of 25. The sentence at the bottom is the real point. The candidate was seventy to a hundred lines of clean, plausible Python. A code review would very probably have approved it. Only running the old program told us the truth.

*[run the candidate through the diamond, or stay on the recorded output]*

## Slide 13 · Reading rules with a model · 1.5 min

Next, what happens if we ask a model to extract the business rules, so that experts can check them? We sent the program and its shared definitions, about 40 thousand characters, to a free model. We asked for rules, each with the lines it comes from. Then we scored the answer against a list of 15 rules that we had verified by hand.

The slide shows the recall, which means how many of the 15 the model found. Nemotron, a model with 120 billion parameters, ran four times and found between 60 and 73 percent. Each run took between one and almost three minutes, and up to nine rules had citations that did not hold up. Laguna, a model from Poolside, ran once, took 55 seconds, and scored 87 percent. That is better, but it is one run. Across three Nemotron runs about a quarter of the covered rules changed, so the answer drifts.

And look at the bottom of the slide. Both models missed the same two rules, truncation and the last account. These are exactly the two rules that matter most for money. This is our own measurement with free models and with hidden reasoning switched off, so a paid model would probably do better.

## Slide 14 · Cited, and still wrong · 1.5 min

This slide shows one rule from one run, and it is the best illustration I have of why citations are not enough.

The rule is number 17, lines 219 to 221. In my words, it says that at the end of the file the program updates the last account's interest. The line numbers are right. The names of the variables are right. Our check for grounding accepted it. And it is wrong, because that branch never runs. The model described what the code says and not what the code does.

It gets worse. Our first scoring script compared rules to the answer list by keywords, and it counted this rule as a correct find of the last account problem. A rule with the opposite meaning scored as a hit. We had to add checks for polarity to the answer list.

That is a lesson for anyone who builds a model as a judge, or a citation check, into a pipeline. These checks tell you where a claim comes from. They do not tell you whether it is true. Only running the code can tell you that.

## Slide 15 · Three ways to generate · 2 min

Now the main result. Same harness, three ways of asking a free model to write the new service. The numbers on the bars are how many of the 25 scenarios matched the old system.

The first group is on the left. We gave the model the list of verified rules, and it wrote Python from that. Three runs, 25 out of 25, every time, in 12 to 85 seconds. That is a strong result. Given a correct specification, a free model wrote code that matches the old system exactly.

The middle group used the model's own extracted rules. The scores were 2, 1 and 0. The candidates raised errors where the old program quietly falls back to a default rate, posted the last account, got the format of the transaction identifier wrong, and in one case crashed.

The right group is the popular approach. The model reads COBOL and writes the new code, with no rules in between. The scores were 1, 3 and 2.

I need to be honest about one more thing. When we later repeated the first group on a clean copy of the repository, two fresh candidates scored only 2 out of 25. The model had written the description text with a slightly different character, one character wrong, in every transaction. The harness caught it. So even the good group is not guaranteed. The takeaway is that the model is a good implementer of a correct specification and a mediocre extractor of the specification, and that only the running program could tell the candidates apart.

## Slide 16 · Who sells what · 1.5 min

Let me give you a very short map of the vendors. This comes from their documentation and announcements. We did not run any of these products, because they need accounts or contracts.

AWS Transform has three paths in one service since March, refactor, replatform and reimagine. Code transformation is free, and so are the assessment and its mainframe agent. IBM's Bob Premium Package for Z, announced on September 30, can be self-hosted on your own OpenShift cluster. It is described as the successor of the watsonx Code Assistant, though I only know that from a secondary source.

Google offers the Mainframe Assessment Tool, which runs in your own cloud project, and Dual Run, which runs the old and new systems side by side and compares the results. Batch is generally available there and online transactions are in preview. Prices are not published. Microsoft has an open source sample of agents, which has no built-in checks, so you have to add your own tests.

Mechanical Orchard's platform verifies new code against captured production data. They publish productivity numbers, such as more than ten thousand lines of verified code per engineer per week. Those are vendor claims. The highlighted tiles on the slide are the ones built around checking.

## Slide 17 · Honest limits · 1.5 min

Before the summary, let me say what you should keep in mind.

Our experiment is one batch program. We have no online screens, and no packed decimal data, because CardDemo ships text extracts and not the original mainframe encoding. So the hardest encodings that real systems have are not in our test.

We used free models with hidden reasoning switched off, and we ran a small number of runs. The numbers show a pattern, but they are not a benchmark. A paid model would likely score higher at extracting rules. I would still not ship its output without the diamond.

We did not run any of the vendor tools. All productivity numbers in this field are vendor claims, for example the sixty percent savings in reverse engineering that one services company reported, or the years to months from AWS. Most prices are not public. The share price drop of IBM I read only through a news site, and a report from the United States government audit office only through a summary.

And for old Java and .NET we only reviewed the tools, such as OpenRewrite and Moderne. We did not run anything. The next step is clear, the same diamond with a Java or .NET upgrade.

## Slide 18 · Three takeaways · 1 min

Three things to remember. One, the running system is the spec. Not the documentation, and not the model's summary of the code.

Two, trust the harness, not the model. We saw a perfectly cited rule that was exactly wrong, and a clean candidate that passed review and failed the check.

Three, models draft and tests judge. Use a model to read code, to propose rules for experts to confirm, and to write code from a verified specification. Do not let it decide whether the new system is equivalent. Free translation makes verification the valuable part of the work. If you remember only one sentence from today, make it this one. The new code is a claim, and the running old system is the evidence.

## Slide 19 · Try it yourself · 1 min

Everything I showed is in our public repository. The address is on the slide with a code to scan, and it points to the folder for this topic.

There are four things you can do there. Run the workshop, which takes about a hundred minutes and is completely free. It uses GnuCOBOL, the open source CardDemo application, and free models from OpenRouter. Try the diamond yourself, because that part needs no model at all and runs in half a second. Compare the vendors with the comparison file. And read the sources, where each claim is marked as verified, as a vendor claim, as secondary, as unpublished, or as measured by us. The participant guide has setup steps, expected output and ideas for extra tasks, for example adding a scenario that breaks our reference.

## Slide 20 · Questions · 2 min

That brings me to the end. To sum it up, translating old code is becoming cheap, and what remains valuable is understanding the old system and proving that the new one behaves the same. Use models for what they do well, and let a running oracle be the judge.

Along the way we looked at a real cost headline, at an open source program that hides a real defect, at the diamond, at a model that cited the code correctly and still got it wrong, and at a clear difference between three ways of generating code. Thank you very much for listening. I would be happy to take your questions now. If I do not know an answer, I will say so and find out, rather than guess.

*[the rest of the two minutes is open for questions]*

---

## Easy questions you may get

These answers are written the same way, so you can read them aloud if you like.

**1. Does the diamond only work for batch jobs?**
Our harness is batch only, because we have no runtime for online screens. The idea carries over, since you capture inputs and outputs for each transaction and compare them. Google's Dual Run lists batch as generally available and online transactions as a preview.

**2. Would a stronger, paid model fix this?**
Probably it would score better at extracting rules. We only used free models with hidden reasoning switched off. But a better model can still be wrong in a convincing way, so I would still want the running old system as the judge.

**3. What if we cannot run the old system at all?**
Then getting it running comes first, and I would price that work before anything else. Without an oracle, equivalence is just an opinion. A test environment or an emulator such as GnuCOBOL can often fill that role.

**4. What about packed decimal and EBCDIC data?**
Our program has none of it, because CardDemo ships text extracts. Real systems do have it, and that is exactly the kind of detail that sits below the business rules. A harness has to include those encodings.

**5. Aren't the rule-based converters enough?**
They give you code that behaves the same, which is a real advantage, but it often looks like COBOL written in Java. Many teams want idiomatic code. In both cases you still want a proof of equivalence for the parts that matter.

**6. What about old Java and .NET?**
We reviewed the tools. OpenRewrite is open source and uses deterministic recipes, Moderne is the commercial layer on top, and GitHub Copilot and AWS Transform have modernization offers. We ran no workshop on them. A good next step is the same diamond for a Java or .NET upgrade.

**7. Which vendor should we pick?**
It depends on the platform. For an AWS-based plan, look at AWS Transform. For an IBM Z estate that stays on Z, look at Bob for Z. For Google Cloud, look at the assessment tool with Dual Run. For a sovereign or multi-cloud case, an open pipeline like ours with self-hosted models is the option.

**8. Was the last account defect planted?**
No. It is in the sample code as published, and we found it by running the job and not by reading it.

**9. How much does the workshop cost?**
Nothing. It uses GnuCOBOL, CardDemo, which is Apache licensed, and free models. Free models are slow, often one to three minutes per call, so plan for waiting.

**10. Are the vendors' productivity numbers true?**
They are claims. We did not reproduce any of them, and I would treat them as a starting point for questions, for example about how equivalence was proven.

---

Sources for the facts above are in [`../research.md`](../research.md), [`../comparison.md`](../comparison.md), [`../workshop-plan.md`](../workshop-plan.md) and [`../workshop/PARTICIPANTS.md`](../workshop/PARTICIPANTS.md).
