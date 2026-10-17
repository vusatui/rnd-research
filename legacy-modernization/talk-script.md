# Talk script: "AI-assisted legacy modernization" (~35 min)

Working title from the outline: *AI won't translate your COBOL for you - but it will help you prove the new system is right.*
Audience: engineers, architects, consultants and pre-sales.

24 slides, 35:00 of planned speaking time including Q&A. The HTML deck is in [`slides/index.html`](slides/index.html). Its speaker notes are built from this file by `slides/build_notes.py`, so edit the notes here first. Likely audience questions with prepared answers are at the end of this file.

**Facts policy.** Every fact comes from [`research.md`](research.md), [`comparison.md`](comparison.md), [`talk-outline.md`](talk-outline.md) and [`workshop-plan.md`](workshop-plan.md) (sources checked and our own runs on 2026-10-17), plus the code and outputs in [`workshop/`](workshop/). Markers follow research.md: ✅ verified on a primary page, 🟡 vendor claim (a vendor or its customer story about itself, not reproduced), 🟠 secondary source only, ❌ not published / unverified, 🧪 measured by us. Say 🟡/🟠/❌ items out loud as claims, not as facts. We did **not** run AWS Transform, Google MAT, IBM Bob or Imogen; everything about them comes from their docs and announcements.

**Presenter keys (deck):** → / Space / PageDown next, ← / PageUp back, Home / End, `N` notes overlay, `S` speaker window (notes, next slide, timer), `O` overview, `F` fullscreen.

| # | Slide | Time | Ends at |
|---|---|---|---|
| 1 | AI-assisted legacy modernization | 0:30 | 0:30 |
| 2 | If translation is free, what are clients paying for? | 1:30 | 2:00 |
| 3 | Why now: the demand signals | 1:45 | 3:45 |
| 4 | Demand signal: EPAM Q2 2026 (public) | 1:30 | 5:15 |
| 5 | A COBOL program is not the system | 1:45 | 7:00 |
| 6 | Four strategies, two technical schools | 1:30 | 8:30 |
| 7 | LLMs read COBOL far better than they write it | 1:45 | 10:15 |
| 8 | Where it breaks: below the business rules | 1:45 | 12:00 |
| 9 | Truncation, not rounding: one missing word | 1:30 | 13:30 |
| 10 | The latent defect the business may rely on | 1:45 | 15:15 |
| 11 | What the harness taught us before any AI ran | 1:30 | 16:45 |
| 12 | The diamond: the running legacy is the spec | 1:45 | 18:30 |
| 13 | Live demo: one batch job, four steps | 1:00 | 19:30 |
| 14 | ex2: rule extraction, measured | 1:45 | 21:15 |
| 15 | Grounded is not correct | 1:15 | 22:30 |
| 16 | ex3 + ex4: three ways to generate, one judge | 2:00 | 24:30 |
| 17 | What the numbers say | 1:15 | 25:45 |
| 18 | Vendor map: mainframe platforms | 1:45 | 27:30 |
| 19 | Deterministic converters and old Java/.NET | 1:30 | 29:00 |
| 20 | Translation is commoditized: follow the money | 1:15 | 30:15 |
| 21 | How we run an engagement | 1:45 | 32:00 |
| 22 | What we did not verify | 1:15 | 33:15 |
| 23 | Takeaways | 0:45 | 34:00 |
| 24 | Questions? | 1:00 | 35:00 |

---

## Slide 1 — AI-assisted legacy modernization
**Timing:** 0:30 (0:00–0:30)
**On slide:**
- Title: AI-assisted legacy modernization
- Subtitle: AI won't translate your COBOL for you - but it will help you prove the new system is right
- Anton Vusatyi · R&D · October 2026
- Repo: github.com/vusatui/rnd-research → legacy-modernization

**Speaker notes:**
Hi, I'm Anton. This talk is about modernizing legacy systems with AI: COBOL on the mainframe first, old Java and .NET briefly at the end. I will cover why clients are coming now, what the big vendors really sell, where language models help and where they silently break behaviour, and what we measured ourselves on a real mainframe batch job. All sources were checked on October 17, 2026. Everything is in the public repo on the slide. When something is only a vendor claim, I will say so.

**Sources:** [README.md](README.md), [talk-outline.md](talk-outline.md)

## Slide 2 — If translation is free, what are clients paying for?
**Timing:** 1:30 (0:30–2:00)
**On slide:**
- Feb 23 2026: Anthropic article "COBOL modernization with AI: breaking the cost barrier" - "quarters instead of years" 🟡
- Next day: IBM shares -13.2%, biggest drop in 25+ years 🟠 (ITPro citing Reuters). IBM: "Translation captures almost none of the actual complexity" 🟠
- Mar 17 2026: AWS Transform - "code transformation is now offered at no cost, replacing the previous lines-of-code based pricing model" ✅
- Question: if translation is free, what are clients paying for?
- Legend: ✅ verified · 🟡 vendor claim · 🟠 secondary · ❌ not published · 🧪 measured by us

**Speaker notes:**
Two headlines from this year. On February 23, Anthropic published an article saying Claude Code can automate the exploration and analysis of COBOL systems, so modernization takes "quarters instead of years". That is a vendor talking about its own product. The next day IBM shares fell 13.2 percent, the biggest drop in more than 25 years. I read that only through ITPro quoting Reuters, so it is marked secondary. IBM's answer was: "translation captures almost none of the actual complexity".

Three weeks later, AWS made mainframe code transformation in AWS Transform free, replacing pricing per line of code. That one I read on the AWS page.

So here is the question for the next 35 minutes. If translating COBOL to Java costs nothing, what exactly are clients going to pay us for? My short answer: understanding the system, and proving the new one does the same thing.

One note on the legend at the bottom. I will use these markers on every slide. Green is verified on a primary page, yellow is a vendor talking about itself, orange is secondary only, red means not published, and the test tube is something we measured ourselves.

**Sources:** [Anthropic article](https://claude.com/resources/articles/how-ai-helps-break-cost-barrier-cobol-modernization), [ITPro](https://www.itpro.com/software/development/anthropic-says-claude-code-can-help-streamline-cost-prohibitive-cobol-modernization-but-ibm-says-its-not-that-simple-decades-of-hardware-software-integration-cannot-be-replicated-by-moving-code) (citing Reuters), [AWS What's New 2026-03-17](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-transform-mainframe-refactor/), [research.md §1–2](research.md)

## Slide 3 — Why now: the demand signals
**Timing:** 1:45 (2:00–3:45)
**On slide:**
- Kyndryl Modernization Report (Oct 1 2026, 2,000 leaders, 12 industries) ✅ survey by a services vendor:
  - **9%** fully understand their application dependencies
  - **nearly half** are behind schedule; 98% say delays hurt
  - 10% use agentic AI in production for modernization; 67% of them on or ahead of track vs 51%
  - "every organization with a mainframe now reports plans to deploy AI to the platform"
- ISG Provider Lens Mainframes US 2026 ✅: GenAI to *extract and validate* rules, SMEs confirm, functional equivalence via parallel automated testing; 56 providers
- GAO-25-107795: 11 critical federal legacy systems, 8 in outdated languages such as COBOL 🟠

**Speaker notes:**
Why are clients asking now? Three signals.

First, Kyndryl surveyed 2,000 leaders in 12 industries, published October 1. Remember that Kyndryl sells modernization services, so read it as a vendor survey. The number I want you to remember: only 9 percent say they fully understand their application dependencies. Nearly half are behind schedule, and 98 percent say delays had a negative impact. Ten percent already use agentic AI in production for modernization, for dependency mapping, code conversion and documentation, and 67 percent of those are on or ahead of track, against 51 percent overall. Also note: every organization with a mainframe reports plans to deploy AI on the platform. Mainframes are not simply being switched off.

Second, ISG's provider report for US mainframes, April 2026. Its description of what enterprises do is almost our talk: use generative AI to extract and validate business rules, have subject-matter experts confirm the logic, and prove functional equivalence with parallel automated testing. 56 providers were evaluated.

Third, the public sector. The GAO reported 11 critical federal legacy systems, 8 of them in outdated languages like COBOL or assembly. I read only a summary of that report, so it is orange.

The pattern: the problem is not "convert my code". It is "I don't know what this does".

**Sources:** [Kyndryl press release](https://www.kyndryl.com/us/en/about-us/news/2026/10/enterprise-it-modernization-trends), [ISG press release](https://ir.isg-one.com/news-market-information/press-releases/news-details/2026/U-S--Enterprises-Accelerate-Mainframe-Modernization/default.aspx), [GAO-25-107795](https://www.gao.gov/products/gao-25-107795), [research.md §1](research.md)

## Slide 4 — Demand signal: EPAM Q2 2026 (public)
**Timing:** 1:30 (3:45–5:15)
**On slide:**
- EPAM Q2 2026 call ✅: financial services +11.5% YoY, fastest-growing vertical; drivers include "mainframe modernization using EPAM IP to reverse engineer, automate and rebuild"
- North America: demand moving from task-based services to "AI-led modernization"; large pipeline deals incl. "legacy mainframe transformation", revenue expected H1 2027 ✅
- Wealth-management client story: >10M LOC reverse-engineered, "60% time savings in reverse engineering effort" 🟡 (vendor claim)
- **MF Lens** = mainframe code analysis and exploration in EPAM AI/Run (CodeMie): Neo4j + PostgreSQL + LiteLLM-proxied model, COBOL preprocessor ✅
- ISG US 2026 leaders list does **not** name EPAM ✅
- EPAM CEO: "Coding gets automated, engineering doesn't" ✅

**Speaker notes:**
Another public demand signal, from a large services vendor. In EPAM's Q2 2026 earnings call, financial services grew 11.5 percent year over year and was their fastest-growing vertical. One of the named drivers was mainframe modernization using EPAM IP to reverse engineer, automate and rebuild, and MF Lens was named. Management also said North American demand is moving from task-based services, like manual testing and front-end work, to AI-led modernization, with large pipeline deals including legacy mainframe transformation, with revenue expected in the first half of 2027.

There is also a client story on that call: a wealth-management client, more than 10 million lines reverse-engineered, with 60 percent time savings in reverse-engineering effort. That is a vendor talking about itself, so it is yellow like any other vendor claim.

MF Lens is documented in the AI/Run CodeMie docs as a mainframe code analysis and exploration solution: a graph database, Neo4j, plus PostgreSQL, a model behind a LiteLLM proxy, and a COBOL preprocessor. Note the architecture: a deterministic graph first, the model on top.

One market fact: ISG's US mainframe report names many leaders, from DXC and Kyndryl to AWS, Google and Heirloom, and EPAM is not among them. And a line from that same call that fits this whole talk: "Coding gets automated, engineering doesn't."

**Sources:** [EPAM Q2 2026 call, Motley Fool transcript](https://www.fool.com/earnings/call-transcripts/2026/08/06/epam-epam-q2-2026-earnings-call-transcript/), [AI/Run CodeMie docs: MF Lens](https://docs.codemie.ai/admin/deployment/extensions/mf-lens/), [ISG press release](https://ir.isg-one.com/news-market-information/press-releases/news-details/2026/U-S--Enterprises-Accelerate-Mainframe-Modernization/default.aspx), [research.md §1](research.md)

## Slide 5 — A COBOL program is not the system
**Timing:** 1:45 (5:15–7:00)
**On slide:**
- Diagram (ex1 output, `out/CBACT04C.mmd`): JCL job INTCALC → CBACT04C → reads TCATBALF, DISCGRP, CARDXREF · updates ACCTDATA · writes SYSTRAN · 5 copybooks · calls CEE3ABD (LE abend service)
- Whole AWS CardDemo tree 🧪: 157 nodes, 385 edges in <1 s (31 programs, 38 JCL, 46 copybooks)
- 16 online programs have dynamic `XCTL PROGRAM(var)` targets static analysis cannot resolve
- `--impact ACCTDATA`: 4 other batch programs also read, write or update the account master
- The real system: JCL, copybooks, VSAM KSDS, CICS/BMS, Db2, assembler helpers, LE services, schedulers

**Speaker notes:**
What does "legacy" actually mean? Our test subject is AWS CardDemo, an open-source credit-card application from AWS, Apache-licensed. And the program we modernize is CBACT04C, the monthly interest-calculation batch job: 652 lines of COBOL.

But the program is not the system. Exercise 1 of our workshop builds a deterministic dependency graph. This diagram is its real output for CBACT04C. A JCL job, INTCALC, runs the program. It reads three VSAM files, updates the account master, writes a transaction file, pulls in five copybooks, and calls CEE3ABD, a Language Environment service, to abend. Every one of those arrows is a place where a rewrite can go wrong.

For the whole CardDemo tree, the graph has 157 nodes and 385 edges, built in under a second. Two details matter. The impact query "who touches ACCTDATA" finds four other batch programs besides ours, so you cannot change the account file layout in isolation. And 16 online programs transfer control to a program whose name is in a variable. Static analysis cannot resolve those. That is the "only 9 percent understand their dependencies" gap in miniature.

In a real estate add CICS screens, Db2, assembler helpers and the scheduler. Lesson one: do discovery deterministically, and let the model explain the graph, not invent it.

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-17), [workshop/ex1_dependency_graph/graph.py](workshop/ex1_dependency_graph/graph.py), [AWS CardDemo](https://github.com/aws-samples/aws-mainframe-modernization-carddemo), [research.md §4](research.md)

## Slide 6 — Four strategies, two technical schools
**Timing:** 1:30 (7:00–8:30)
**On slide:**
- Four strategies: **rehost / replatform** (same code, new runtime) · **refactor** (deterministic conversion) · **reimagine / rewrite** (new idiomatic code) · **replace** (buy a package)
- Deterministic transpilers: Heirloom, AWS Transform *refactor* (ex-Blu Age), TSRI, Astadia, CloudFrame, mLogica → provable but non-idiomatic code
- LLM "reimagine" pipelines: AWS Transform *reimagine* + Kiro / Claude Code, Google MAT, IBM Bob for Z, Microsoft open-source agents, Mechanical Orchard → idiomatic code that must be proven
- Converging: LLMs + deterministic analysis + an **executable oracle**

**Speaker notes:**
There are four classic strategies. Rehost or replatform: keep the COBOL, move it to a new runtime. Refactor: convert it mechanically into Java, keeping the structure. Reimagine, or rewrite: produce new, idiomatic code in a modern stack. And replace: buy a package and retire the code.

For the middle two there are two technical schools. The deterministic transpilers, like Heirloom, AWS Transform's refactor path, which is the former Blu Age, TSRI, Astadia, CloudFrame and mLogica. They give you code you can trust to behave the same, but it often reads like COBOL written in Java. Heirloom's own phrase is that it "compiles, not translates".

The second school is LLM-based reimagine pipelines: AWS Transform's reimagine pattern with an agentic coder like Kiro or Claude Code, Google's Mainframe Assessment Tool, IBM Bob for Z, Microsoft's open-source agents, and Mechanical Orchard. They give you idiomatic code, and then you have to prove it is right.

The interesting part is that the two schools are converging. Everyone now combines an LLM with deterministic analysis and some executable oracle that says what correct means. Keep the word "oracle"; it comes back in ten minutes.

**Sources:** [research.md TL;DR §3, §2](research.md), [comparison.md](comparison.md), [AWS What's New 2026-03-17](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-transform-mainframe-refactor/), [Heirloom: LLMs and COBOL](https://heirloomcomputing.com/llms-and-cobol-modernization/)

## Slide 7 — LLMs read COBOL far better than they write it
**Timing:** 1:45 (8:30–10:15)
**On slide:**
- COBOL-Coder paper (Concordia + FPT, arXiv 2604.03986) ✅, compile % / pass@1:
  - COBOL → Java (143 HumanEval-style pairs): GPT-4o **97.2 / 85.3**, gpt-oss-120B 98.6 / 89.5
  - Java → COBOL: GPT-4o **4.4 / 2.2**
  - Writing COBOL (COBOLEval): GPT-4o 41.8 / 16.4; COBOL-Coder-14B 73.95 / 49.33; most open models 0
- Authors: single-file tasks, no copybooks / JCL / cross-program dependencies; practitioners see LLM output as "junior developer drafts"
- Good at: explaining, dependency/impact analysis on top of a graph, rule extraction with citations, test generation, forward engineering of small specified units
- Microsoft's early GPT-4 attempts: "a good mix of educated guesses ... and hallucinational gibberish" ✅

**Speaker notes:**
So where is AI actually good? The best recent evidence I found is the COBOL-Coder paper from Concordia University and FPT, 2026.

On a set of 143 small HumanEval-style programs, translating COBOL into Java works remarkably well: GPT-4o compiles 97 percent and passes the tests 85 percent of the time; the open gpt-oss-120B is slightly better. Now reverse the direction. Java into COBOL: GPT-4o compiles 4.4 percent and passes 2.2. Writing COBOL from scratch on COBOLEval: 42 percent compile, 16 percent pass for GPT-4o, and most open models score zero. A fine-tuned 14B model gets to 74 and 49.

So: models read COBOL far better than they write it. But look at the authors' own caveat. These are single files, without copybooks, JCL or calls to other programs. And, as the authors report, practitioners see model output as junior-developer drafts and list restartability, file status and SQLCODE handling as adoption requirements. That is system behaviour, and no benchmark measures it.

Microsoft's dev blog is refreshingly honest about its first GPT-4 attempts: "a good mix of educated guesses and hallucinational gibberish".

Where AI is good, then: explaining code, impact analysis on top of a real graph, extracting rules with line citations, generating tests, and writing small units from a precise spec. Keep that last point in mind for the demo.

**Sources:** [arXiv 2604.03986](https://arxiv.org/abs/2604.03986), [MS dev blog](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/), [research.md §3](research.md)

## Slide 8 — Where it breaks: below the business rules
**Timing:** 1:45 (10:15–12:00)
**On slide:**
- Failures live below the business rules: sign overpunch / packed decimal · truncation vs rounding · VSAM KSDS key semantics · LOW-VALUES · abend codes · uninitialized storage · latent defects the business relies on
- Mechanical Orchard on AWS CardDemo (field CTO, Jun 2026) ✅ article / 🟡 their experiment - an LLM-only Java replica compiled and ran, but:
  - treated a KSDS as a flat file
  - wrote negatives as "-" strings instead of sign overpunch
  - dropped a COBDATFT branch
  - replaced abend 999 with exit 12
- Their conclusion: modernization is a verification problem

**Speaker notes:**
Here is the core of the talk. Business rules are the part everyone talks about: the interest formula, the fee, the eligibility check. Models are decent at those. The failures live below the business rules: how a negative number is encoded in the last digit, sign overpunch, or packed decimal; whether a division truncates or rounds; what a keyed VSAM file does that a flat file does not; LOW-VALUES; abend codes that operators and schedulers react to; uninitialized storage; and bugs that the business has quietly built processes around.

Mechanical Orchard published a nice experiment in June, also on AWS CardDemo. Their field CTO had a model write a Java replica of a CardDemo program. It compiled, it ran, it looked fine. But it treated a keyed VSAM file as a flat file. It wrote negative numbers as minus-sign strings instead of overpunch. It dropped a branch that calls COBDATFT. And it replaced abend 999 with exit code 12. Every one of these would break a downstream job or an operator's runbook.

Mechanical Orchard sells verification, so this is their experiment, not reproduced by us. But the next three slides show we hit the same class of problems ourselves, on a different CardDemo program.

**Sources:** [Mechanical Orchard: Modernization is a verification problem](https://www.mechanical-orchard.com/research/mainframe-modernization-is-a-verification-problem), [research.md TL;DR §4, §2](research.md), [talk-outline.md](talk-outline.md)

## Slide 9 — Truncation, not rounding: one missing word
**Timing:** 1:30 (12:00–13:30)
**On slide:**
- COBOL (CBACT04C, 1300-COMPUTE-INTEREST): `COMPUTE WS-MONTHLY-INT = (TRAN-CAT-BAL * DIS-INT-RATE) / 1200` - no `ROUNDED`, so the result is truncated
- Reference Python: `.quantize(CENT, rounding=ROUND_DOWN)`
- Real diamond output 🧪 for an LLM candidate written from COBOL only (`ROUND_HALF_UP`):
  - `tx#1 amount: legacy=12.49 modern=12.50`
  - `tx#5 amount: legacy=0.99 modern=1.00`
  - `tx#9 amount: legacy=12499999.99 modern=12500000.00`
  - `acct 00000000009 curr_bal: legacy=560.00 modern=12500560.00`
- One cent per transaction, every month, on every account

**Speaker notes:**
The first example. This is the actual interest line in CBACT04C: balance times rate, divided by 1200. What matters is the word that is not there: ROUNDED. Without it, COBOL truncates the result to the target field's two decimals. Our reference implementation does the same with ROUND_DOWN.

Now the bottom half is real output from our diamond, exercise 4. This candidate was written by a free model that got only the COBOL source, no rule list. It used ROUND_HALF_UP, the "natural" choice for money in Python. The legacy writes 12.49, the candidate 12.50. 0.99 becomes 1.00. And look at the last line: on one account the candidate posted 12.5 million of interest to the balance where the legacy posted nothing. That is the next slide's defect.

One cent sounds small. It is one cent per transaction, every month, on every account, and it makes reconciliation with the general ledger fail. And none of the models in our rule-extraction runs listed truncation as a rule.

**Sources:** [workshop/ex3_new_service/interest.py](workshop/ex3_new_service/interest.py), [workshop/ex4_equivalence/diamond.py](workshop/ex4_equivalence/diamond.py), [workshop-plan.md](workshop-plan.md) (measured 2026-10-17), [AWS CardDemo](https://github.com/aws-samples/aws-mainframe-modernization-carddemo)

## Slide 10 — The latent defect the business may rely on
**Timing:** 1:45 (13:30–15:15)
**On slide:**
- Main loop (simplified): `PERFORM UNTIL END-OF-FILE = 'Y'` · `IF END-OF-FILE = 'N'` read next, post previous account on key change · `ELSE PERFORM 1050-UPDATE-ACCOUNT`
- The `ELSE` is unreachable: the loop exits at EOF first → **the last account's interest is never posted** to its balance (the interest transactions are still written)
- A "clean" re-implementation that fixes it: equivalent on **9/25** scenarios (fails 16/25) 🧪
- Bug-for-bug or fix? A **business decision**, made explicitly and documented
- Found by running the legacy, not by reading it

**Speaker notes:**
The second example is my favourite, because it is a real defect in the sample code that nobody had to plant.

The main loop runs until end of file. Inside, if not at end of file, it reads the next record and, when the account number changes, posts the previous account's interest. There is an ELSE branch that posts the last account at end of file. It reads perfectly. But the PERFORM UNTIL checks the condition first, so when end of file is reached the loop exits and the ELSE never runs. The last account in the file gets its interest transactions written, but its balance is never updated.

We found this while building the harness, by running the program, not by reading it. When we ran our reference implementation with the defect fixed, it was equivalent on only 9 of 25 scenarios.

So what do you do? In a real bank, some process may have grown around this: a manual correction, a reconciliation report. Replicating the bug or fixing it is not an engineering decision. It is a business decision, and the point is to make it explicitly, with the diff in hand, rather than discover it in production. A model that "helpfully" fixes it for you has made that decision without asking.

**Sources:** [workshop/ex3_new_service/interest.py](workshop/ex3_new_service/interest.py) (`legacy_compat`), [workshop-plan.md](workshop-plan.md) (measured 2026-10-17), [research.md §4](research.md)

## Slide 11 — What the harness taught us before any AI ran
**Timing:** 1:30 (15:15–16:45)
**On slide:**
- Setup 🧪: CardDemo commit `59cc6c2`, CBACT04C compiled **unchanged** with GnuCOBOL 3.2 (`-std=ibm -fsign=EBCDIC`); VSAM KSDS as GnuCOBOL indexed files; `CEE3ABD` and JCL `PARM` shimmed; build ~1 s, one run ~20 ms
- **Abend 999 → exit status 231** on Linux (999 mod 256): an operator watching for 999 sees nothing
- **LOW-VALUES**: `STRING ... INTO` leaves x'00' in the rest of the 100-byte `TRAN-DESC`; byte-exact `--strict` fails on it (6/8 scenarios) until the comparison schema decides
- **Sample data proves nothing**: CardDemo's category balances are all zero, almost any candidate passes → generated scenarios required
- **Our own bug**: our REST API returned money as JSON floats and `-0.0` for a truncated negative cent; the legacy record has no negative zero. Caught by a test, fixed

**Speaker notes:**
Before we let any model write code, we had to get the legacy running on a laptop. We took CardDemo at a pinned commit and compiled CBACT04C unchanged with the open-source GnuCOBOL 3.2 in IBM mode. Keyed VSAM files are emulated with GnuCOBOL's indexed files, and two mainframe services are shimmed: the Language Environment abend call and the JCL PARM. The build takes about a second and one run about 20 milliseconds.

Building that harness taught us four things.

One: abend 999 shows up on Linux as process exit status 231, because exit codes are taken modulo 256. If your scheduler or operator watches for 999, they see nothing.

Two: the transaction description is built with STRING INTO, which leaves binary zeros, LOW-VALUES, in the rest of the 100-byte field instead of spaces. A byte-exact comparison fails on it until you decide, in the comparison schema, what equivalence means for that field.

Three: CardDemo's sample category balances are all zero. Zero times any rate is zero. So "it matches on the sample data" proves nothing; you need generated scenarios.

Four, and this one is on us: our own REST API first returned money as JSON floats, and minus zero for a truncated negative cent. The legacy record has no negative zero. A test caught it.

None of this needed AI. All of it would break a cutover.

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-17), [workshop/legacy/](workshop/legacy/), [workshop/README.md](workshop/README.md), [research.md §4](research.md)

## Slide 12 — The diamond: the running legacy is the spec
**Timing:** 1:45 (16:45–18:30)
**On slide:**
- Diagram: same input → running COBOL (oracle) and new code → byte-level compare with a per-field schema → equivalent / diff
- Our `ex4`: 25 scenarios (CardDemo data, edge amounts, single account, 20 generated, 2 abend paths); timestamps masked, FILLER ignored, `--strict` for byte-exact; full run of both sides 0.5–0.7 s 🧪
- Productized diamonds ✅: Google **Dual Run** (replay production, compare outputs; batch GA, online preview) · Mechanical Orchard **Imogen** (verify against captured production data flows, slice by slice) · IBM wca4z (generated unit tests for semantic equivalence)
- Key message: **trust the harness, not the model's account of what it did**

**Speaker notes:**
This is the pattern that ties it together. Mechanical Orchard calls it the diamond. You feed the same input to the running legacy program, which is your oracle, and to the new code. Then you compare the outputs byte by byte, with a schema per field that says what equivalence means: timestamps are masked, filler is ignored, and you can switch to strict byte-exact mode. Anything that differs is a diff you either fix or approve.

Our exercise 4 is exactly that, in about a hundred lines. Twenty-five scenarios: the CardDemo sample data, edge amounts, a single account, twenty generated random portfolios, and two abend paths. Both sides for all 25 run in well under a second, so it fits in CI on every commit.

The big vendors sell productized diamonds. Google's Dual Run runs the mainframe and the cloud side by side and replays production events; batch is generally available, online transactions in preview. Mechanical Orchard's Imogen verifies new code against captured production data flows, slice by slice. IBM's code assistant generates unit tests to compare semantic equivalence.

The message I want you to repeat to clients: the running legacy is the spec. And trust the harness, not the model's account of what it did.

**Sources:** [workshop/ex4_equivalence/diamond.py](workshop/ex4_equivalence/diamond.py), [workshop/ex4_equivalence/scenarios.py](workshop/ex4_equivalence/scenarios.py), [Google Dual Run overview](https://docs.cloud.google.com/mainframe-dual-run/docs/dual-run-overview), [Imogen platform](https://www.mechanical-orchard.com/platform), [IBM watsonx Code Assistant for Z](https://www.ibm.com/products/watsonx-code-assistant-z), [workshop-plan.md](workshop-plan.md)

## Slide 13 — Live demo: one batch job, four steps
**Timing:** 1:00 (18:30–19:30)
**On slide:**
- 1 **ex1 dependency graph**: deterministic; `--focus CBACT04C --impact ACCTDATA`
- 2 **ex2 rule extraction**: LLM returns rules with line citations; grounding check + recall vs a hand-verified answer key (15 rules)
- 3 **ex3 new service**: LLM generates the service three ways: from verified rules / from LLM-extracted rules / from COBOL only
- 4 **ex4 diamond**: every candidate against the running COBOL, 25 scenarios
- All free: GnuCOBOL, CardDemo (Apache-2.0), free OpenRouter models (reasoning off); fallback: recorded results on the next slides

**Speaker notes:**
Now the demo, from the workshop folder. Four steps, the same four steps an engagement has. Exercise 1 is the deterministic graph you already saw. Exercise 2 asks a model to extract business rules with line citations, and checks them two ways: are the citations real, and how many of 15 hand-verified rules did it find. Exercise 3 generates the new service three ways: from the verified rule list, from the model's own extracted rules, and from the COBOL alone. Exercise 4 runs every candidate through the diamond.

Everything is free: GnuCOBOL, CardDemo, and free models on OpenRouter. Free models are slow, often one to five minutes per call, and rate-limited, so for the talk I will run the deterministic parts live and show the recorded results from October 17 for the model calls. They are on the next slides.

**Sources:** [workshop-plan.md](workshop-plan.md), [workshop/README.md](workshop/README.md), [comparison.md](comparison.md) (open-source pipeline)

## Slide 14 — ex2: rule extraction, measured
**Timing:** 1:45 (19:30–21:15)
**On slide:**
- CBACT04C + copybooks, ~40k-char prompt, free models, reasoning off 🧪
- `nvidia/nemotron-3-super-120b-a12b:free`, 4 runs: 78–163 s per run, 25–43 rules, 0–9 ungrounded, **recall 0.60–0.73**
- `poolside/laguna-s-2.1:free`, 1 run: 55 s, 20 rules, 1 ungrounded, **recall 0.87**
- Drift across 3 nemotron runs (1 − Jaccard of covered rules): **0.25**
- Always missed: **TRUNCATION**, **LAST_ACCOUNT_NOT_POSTED** (nemotron also NEGATIVE_BALANCE): exactly the two rules that matter most for money

**Speaker notes:**
Exercise 2 results. We send CBACT04C and its copybooks, about 40 thousand characters, to a free model and ask for business rules, each with the line range it comes from.

Nemotron 3 Super, a 120-billion-parameter model, four runs: one to almost three minutes per run, between 25 and 43 rules, up to 9 of them with citations that do not hold up, and recall between 0.60 and 0.73 against our answer key of 15 hand-verified rules. Poolside's Laguna, one run: 55 seconds, 20 rules, one ungrounded, recall 0.87. Better, but a single run.

Two more numbers. Drift: across three runs of the same model on the same input, a quarter of the covered rules changed. Rules like the fee stub or skipping a zero rate appear in one run and disappear in the next.

And the line that matters: no run found truncation instead of rounding, and no run found that the last account is never posted. Those are the two rules with direct money impact, and both are "below the business rules". The model found the business rules and missed the behaviour.

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-17), [workshop/ex2_rule_extraction/extract.py](workshop/ex2_rule_extraction/extract.py), [workshop/ex2_rule_extraction/gold_rules.json](workshop/ex2_rule_extraction/gold_rules.json)

## Slide 15 — Grounded is not correct
**Timing:** 1:15 (21:15–22:30)
**On slide:**
- One extracted rule, with correct line citations and correct symbols 🧪:
  - > R17 [219-221] "When END-OF-FILE is 'Y' (after loop exit), the program performs 1050-UPDATE-ACCOUNT to persist the last account's accumulated interest."
- Grounded ✅ - and **wrong** ❌: the `ELSE` branch is unreachable
- Our first keyword scorer counted it as a hit → the answer key now has **polarity checks** (`require_any`)
- Lesson for LLM-as-judge and citation checks: they verify *where*, not *whether*

**Speaker notes:**
This slide is one rule from one run, and it is the best illustration I have of why citations are not enough.

Rule 17, lines 219 to 221: "When end of file is Y, after loop exit, the program performs 1050-UPDATE-ACCOUNT to persist the last account's accumulated interest." The line numbers are right. The symbols are right. Our grounding check passed it. And it is exactly wrong, because that branch never runs. The model described what the code says, not what it does.

It gets worse. Our first scorer matched rules against the answer key by keywords, and it counted this rule as finding the last-account rule. The opposite meaning scored as a hit. We had to add polarity checks to the answer key.

That is a lesson for anyone building LLM-as-judge or citation checks into a pipeline: they check where a claim comes from, not whether it is true. Only execution tells you that.

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-17), [workshop/ex2_rule_extraction/gold_rules.json](workshop/ex2_rule_extraction/gold_rules.json)

## Slide 16 — ex3 + ex4: three ways to generate, one judge
**Timing:** 2:00 (22:30–24:30)
**On slide:**
- Chart: equivalent scenarios out of 25 (diamond vs running COBOL) 🧪
  - Hand-written reference: **25/25**
  - Reference with the defect fixed: **9/25** (a business decision)
  - LLM from **verified** rules, 3 runs (nemotron-3-super): **25, 25, 25** (12–85 s each)
  - LLM from **LLM-extracted** rules, 3 rule sets: **2, 1, 0**
  - LLM from **COBOL only**, 3 runs (gemma-4-31b, nemotron ×2): **1, 3, 2**
- Caught: abends where legacy falls back to the `DEFAULT` rate · rate looked up once per account · last account posted · tx id format · `ROUND_HALF_UP` · `.get()` instead of abend 999 · transaction order/count · an `UnboundLocalError` crash

**Speaker notes:**
Now the main result. Same diamond, five kinds of candidate.

Our hand-written reference: 25 of 25. With the last-account defect fixed: 9 of 25, the business decision from before.

A free model, Nemotron, writing the service from the verified rule list: 25 of 25, three times out of three, in 12 to 85 seconds per generation. That is a strong result. Given a correct spec, a free model wrote byte-equivalent code.

The same model writing from rules that a model extracted: 2, 1 and 0 out of 25. It raised abends where the legacy quietly falls back to a DEFAULT rate; it looked up the rate once per account instead of per category; it posted the last account; it got the transaction id format wrong; one candidate crashed with an UnboundLocalError.

And the "just translate it" path, model reads COBOL and writes Python, three runs with Gemma and Nemotron: 1, 3 and 2 out of 25. Rounding instead of truncation, the last account posted, a dictionary get with a default instead of abend 999, and different transaction order and count.

Every one of these candidates is 70 to 100 lines of clean, plausible Python. Without the diamond you would have approved most of them in code review.

**Sources:** [workshop-plan.md](workshop-plan.md) (measured 2026-10-17), [workshop/ex3_new_service/generate.py](workshop/ex3_new_service/generate.py), [workshop/ex4_equivalence/diamond.py](workshop/ex4_equivalence/diamond.py)

## Slide 17 — What the numbers say
**Timing:** 1:15 (24:30–25:45)
**On slide:**
- 1 The LLM is a good **implementer** of a correct spec and a mediocre **extractor** of the spec
- 2 "LLM reads COBOL, LLM writes Java" fails on exactly the money-relevant details
- 3 Only the running COBOL told us which candidate is right; code review of 70–100-line candidates would have missed most of it
- Caveats: one program, batch only, free models with reasoning off, small sample; no CICS/BMS, no EBCDIC files or COMP-3 in this program

**Speaker notes:**
Three takeaways from the demo, straight from our workshop notes.

One: the model is a good implementer of a correct spec and a mediocre extractor of the spec. So put the human effort, with subject-matter experts, into the spec, and let the model write code against it.

Two: the popular pipeline, model reads COBOL, model writes Java, fails on exactly the details that move money. This matches the benchmark from slide 7: good at small units, blind to system behaviour.

Three: only the running COBOL told us which candidate was right.

And the honest caveats. This is one batch program, with free models and hidden reasoning switched off. There is no CICS or BMS online runtime in our harness, and this program has no EBCDIC files or packed decimal, because CardDemo ships ASCII extracts. A paid frontier model would probably score higher on extraction. I would still not ship it without the diamond.

**Sources:** [workshop-plan.md](workshop-plan.md) (takeaways), [comparison.md](comparison.md) (limits of the open pipeline)

## Slide 18 — Vendor map: mainframe platforms
**Timing:** 1:45 (25:45–27:30)
**On slide:**
- Table (from comparison.md):
  - **AWS Transform for mainframe**: managed agentic service; COBOL, PL/I, JCL, CICS, BMS, Db2, VSAM, IMS TM; refactor → Java (ex-Blu Age) or reimagine via Kiro / Claude Code; AWS regions only ✅
  - **IBM Bob Premium Package for Z** (ex watsonx Code Assistant for Z): IDE agent + deterministic app understanding; COBOL/PL/I → Java, or optimize in place; **self-hosted on customer OpenShift** (Sep 30 2026) ✅
  - **Google MAT + Dual Run**: Gemini-based assessment in your GCP project, MCP server; Dual Run parallel run ✅; pricing ❌
  - **Microsoft Legacy-Modernization-Agents**: open source, COBOL → Java Quarkus or C# .NET; no built-in verification ✅
  - **Mechanical Orchard Imogen**: platform + delivery team; diamond against captured production data ✅; ">10,000 lines of verified code per engineer per week" 🟡

**Speaker notes:**
Now the vendor map. I will not read the table; here is how to think about each.

AWS Transform for mainframe is the broadest managed service: it covers COBOL, PL/I, JCL, CICS, BMS screens, Db2, VSAM and IMS. Since March it has three patterns in one service: deterministic refactor to Java, replatform, and reimagine with an agentic coder. It runs only in AWS regions.

IBM replaced watsonx Code Assistant for Z with Bob Premium Package for Z. It is an agent in the IDE with deterministic application understanding underneath. The important news from September 30: it can be self-hosted on the customer's OpenShift with approved models. For regulated clients who cannot send code to a cloud model, that matters. That Bob is the successor of watsonx Code Assistant comes only from a search summary, so it is orange.

Google has the Mainframe Assessment Tool, Gemini-based, which you deploy in your own project, and it exposes an MCP server for agents. Plus Dual Run for parallel running. No published prices.

Microsoft has open-source agents as a sample: good for proofs of concept and teaching, but verification is up to you.

And Mechanical Orchard sells a platform plus a delivery team, built around the diamond. Their "more than ten thousand lines of verified code per engineer per week" is their own claim.

**Sources:** [comparison.md](comparison.md), [AWS Transform docs](https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe.html), [IBM Bob for Z announcement 2026-09-30](https://www.ibm.com/new/announcements/ibm-bob-premium-package-for-z-expands-with-on-premises-deployment-and-new-saas-capabilities), [Google MAT settings](https://docs.cloud.google.com/mainframe-assessment-tool/docs/configure-settings), [MAT MCP server](https://docs.cloud.google.com/mainframe-assessment-tool/docs/mcp-server), [Legacy-Modernization-Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents), [Imogen Summer 2026](https://www.mechanical-orchard.com/insights/whats-new-in-imogen-the-summer-2026-release)

## Slide 19 — Deterministic converters and old Java/.NET
**Timing:** 1:30 (27:30–29:00)
**On slide:**
- Classic converters, now adding AI on top: Heirloom (COBOL→Java transpiler + runtime for CICS, JCL, VSAM, IMS ✅; AI refactoring after a deterministic baseline 🟡) · AWS Transform refactor (ex-Blu Age) ✅ · TSRI, Astadia, CloudFrame, Rocket / OpenText 🟠 · mLogica via AWS: Assembler→COBOL **$2.75 / LOC** ✅
- Old Java / .NET:
  - **OpenRewrite** (open source, deterministic recipes) / **Moderne** (agent picks and composes recipes): Java 8→25, Spring, .NET; "$250K typical", "$2M typical" enterprise ✅
  - **GitHub Copilot modernization**: Java, .NET, C++ upgrades + Azure migration, uses OpenRewrite; not COBOL ✅
  - **AWS Transform for .NET**: .NET Framework → cross-platform .NET, free within 50k agent-minutes/month ✅
- Same idea everywhere: deterministic recipe or transpiler first, LLM on top, build and tests as the check

**Speaker notes:**
Two more families.

The classic deterministic converters existed long before LLMs and are now adding AI on top. Heirloom transpiles COBOL to Java and ships a runtime for CICS, JCL, VSAM and IMS. Its own argument is that models belong on documentation, tests and refactoring after a deterministic baseline. AWS's refactor path, the former Blu Age, is in the same family. TSRI, Astadia, CloudFrame and the Rocket and OpenText runtimes I know only from secondary sources. One published price for scale: mLogica's Assembler to COBOL conversion through AWS is 2 dollars 75 per line.

For old Java and .NET, the picture is simpler because the target languages are close. OpenRewrite is open source with deterministic recipes, for example Java 8 to 25 or Spring upgrades. Moderne is the commercial version, where an agent picks and composes recipes; their pricing page says 250 thousand dollars typical, and 2 million typical for enterprise. GitHub Copilot's modernization uses OpenRewrite under the hood for Java and .NET upgrades; it does not do COBOL. AWS Transform for .NET ports .NET Framework to modern .NET, free within 50 thousand agent minutes a month.

The common pattern again: deterministic transformation first, the model on top, and the build and tests as the check. We did not run a Java or .NET workshop; that is a follow-up.

**Sources:** [comparison.md](comparison.md), [Heirloom: LLMs and COBOL](https://heirloomcomputing.com/llms-and-cobol-modernization/), [AWS Mainframe Modernization pricing](https://aws.amazon.com/mainframe-modernization/pricing/), [Moderne pricing](https://moderne.ai/pricing), [OpenRewrite](https://moderne.ai/openrewrite), [Copilot modernization](https://learn.microsoft.com/en-us/azure/developer/github-copilot-app-modernization/overview), [AWS Transform pricing](https://aws.amazon.com/transform/pricing/)

## Slide 20 — Translation is commoditized: follow the money
**Timing:** 1:15 (29:00–30:15)
**On slide:**
- AWS Transform: assessment + mainframe agent **free**; custom transformation agent **$0.035 / agent-minute**; refactored-app runtime **$0.31 per CPU core-hour** ✅
- IBM: per authorized user + tokens; 1 resource unit = 150k tokens ≈ 5,000–7,000 COBOL lines ✅; ~€1,454 per user list 🟠
- Google MAT / Dual Run, Mechanical Orchard, Heirloom, TSRI, CloudFrame: **not published** ❌
- Positioning: differentiate on **discovery quality, the equivalence harness, data migration and cutover** (e.g. graph tools such as EPAM MF Lens + delivery)
- Pick per client platform: AWS → Transform (+ Imogen-style verification) · IBM Z staying on Z → Bob for Z · GCP → MAT + Dual Run · sovereign / multi-cloud → open pipeline with self-hosted models

**Speaker notes:**
Follow the money. AWS gives away assessment and the mainframe transformation agent. You pay 3.5 cents per agent minute for custom transformations and 31 cents per CPU core per hour to run the refactored application. IBM charges per user plus tokens, and gives a useful conversion factor: one resource unit is 150 thousand tokens, roughly 5 to 7 thousand lines of COBOL. A reseller lists about 1,450 euros per user. Most of the others don't publish prices.

So the translation itself is close to free. What is not free, and what nobody can give away, is understanding a client's estate, building the harness that proves equivalence, migrating the data, and running the cutover without stopping the business. That is where a services company earns its money: discovery, verification and cutover — the same space tools like EPAM MF Lens target on the analysis side.

Practical pairing by platform: an AWS client, use Transform and add Imogen-style verification. An IBM Z shop that stays on Z, Bob for Z, self-hosted if needed. A GCP client, the Assessment Tool plus Dual Run. Sovereign or multi-cloud, an open pipeline like our workshop with self-hosted models; self-hosted Bob is the only big-vendor option we found.

**Sources:** [AWS Transform pricing](https://aws.amazon.com/transform/pricing/), [AWS Mainframe Modernization pricing](https://aws.amazon.com/mainframe-modernization/pricing/), [IBM license guide](https://www.ibm.com/docs/en/watsonx/watsonx-code-assistant-4z/2.x?topic=information-license-guide-watsonx-code-assistant-z), [Bücker GmbH reseller page](https://bueckergmbh.de/Kauf-IBM-D0GQ3ZX/IBM-watsonx-Code-Assistant-for-Z-for-IBM-Z-Authorized-User-Subscription-License), [comparison.md](comparison.md) (how to position)

## Slide 21 — How we run an engagement
**Timing:** 1:45 (30:15–32:00)
**On slide:**
- 1 Inventory and dependency graph, deterministic (ex1-style scanner; commercial options include EPAM MF Lens)
- 2 Get the oracle running: a test LPAR, or a GnuCOBOL / Micro Focus harness. No oracle → price the harness work first
- 3 Capture production-like inputs; generate scenarios (sample data is all zeros)
- 4 Extract rules with an LLM, with citations; verify with SMEs; keep the answer key
- 5 Generate code per slice from **verified** rules
- 6 Diamond in CI: per-field comparison schema, abend paths included
- 7 Strangler cutover with parallel run; decide **bug-for-bug vs fix** explicitly, per defect

**Speaker notes:**
So how do we run an engagement? Seven steps, and each one maps to something you saw.

One, inventory and dependency graph, deterministic. A scanner like exercise 1, or a commercial graph tool such as EPAM MF Lens. The model explains the graph; it does not build it.

Two, get the oracle running before anything else. A test LPAR at the client, or a harness on GnuCOBOL or Micro Focus. If the client cannot give you a running legacy or data, price the harness work first, because everything else depends on it.

Three, capture production-like inputs and generate scenarios. Remember the sample data that was all zeros.

Four, extract rules with a model, with line citations, then verify them with the client's subject-matter experts. That verified list is the most valuable artefact of the project. Keep it as an answer key.

Five, generate code slice by slice from the verified rules. That is where models are good.

Six, the diamond runs in CI, with a comparison schema per field and the abend paths included.

Seven, cut over with a strangler pattern and parallel run. And for every defect you find, like the last account, decide bug-for-bug or fix explicitly, with the business, in writing.

**Sources:** [talk-outline.md](talk-outline.md) §9, [comparison.md](comparison.md) (how to position), [workshop-plan.md](workshop-plan.md)

## Slide 22 — What we did not verify
**Timing:** 1:15 (32:00–33:15)
**On slide:**
- We did **not** run AWS Transform, Google MAT, IBM Bob or Imogen (accounts / contracts needed); all vendor facts come from docs
- All productivity numbers are vendor claims 🟡: EPAM's "60% time savings", Mechanical Orchard 10k LOC/week and 11,578 LOC in 28 hours, AWS "years to months"
- Prices not public ❌: Google MAT / Dual Run, IBM Bob for Z, Mechanical Orchard, Heirloom, TSRI, CloudFrame
- Secondary only 🟠: IBM share drop (Reuters paywalled), GAO report (summary)
- Our workshop: one batch program, free models, no online (CICS/BMS) runtime, no EBCDIC / COMP-3 data
- Old Java/.NET: tooling reviewed, no workshop yet (next: Java 8 → 21 / .NET Framework → .NET 8 with OpenRewrite + an LLM, same diamond)

**Speaker notes:**
Before the summary, what I did not verify, so you can calibrate everything I said.

We did not run any of the big platforms: AWS Transform, Google's tool, IBM Bob or Imogen. They need accounts or contracts. Everything about them comes from their documentation and announcements.

Every productivity number in this space is a vendor claim: EPAM's 60 percent reverse-engineering savings, Mechanical Orchard's ten thousand lines per engineer per week and their 11,578 lines in 28 hours, AWS's "years to months".

Most prices are not public. The IBM share drop and the GAO report I read only through secondary sources.

Our own workshop is one batch program with free models, no online CICS runtime and no EBCDIC or packed-decimal data. And for old Java and .NET we reviewed the tooling but ran nothing. The obvious next step is a Java 8 to 21 or .NET Framework to .NET 8 migration with OpenRewrite plus a model, and the same diamond.

**Sources:** [research.md §5](research.md) (open items), [comparison.md](comparison.md), [Mechanical Orchard: first year of Imogen](https://www.mechanical-orchard.com/insights/reflections-on-the-first-year-of-imogen)

## Slide 23 — Takeaways
**Timing:** 0:45 (33:15–34:00)
**On slide:**
- **The running legacy is the spec**
- **Trust the harness, not the model's account of what it did**
- **Free translation makes verification the product**
- Use AI to read, extract and implement from a verified spec; never as the judge of equivalence

**Speaker notes:**
Three sentences to take away. The running legacy is the spec, not the documentation and not the model's summary. Trust the harness, not the model's account of what it did; we saw a perfectly cited rule that was exactly wrong. And free translation makes verification the product; that is our business. Use models to read, to extract rules for experts to confirm, and to implement from a verified spec. Never let them be the judge of equivalence.

**Sources:** [talk-outline.md](talk-outline.md) (key messages), [research.md TL;DR](research.md)

## Slide 24 — Questions?
**Timing:** 1:00 (34:00–35:00)
**On slide:**
- Research, vendor comparison, workshop (4 exercises, all free), this deck and the script
- https://github.com/vusatui/rnd-research/tree/main/legacy-modernization
- Anton Vusatyi

**Speaker notes:**
Thank you. Everything is in the repo: the research notes with verification markers, the vendor comparison, the workshop you can run on a laptop with GnuCOBOL and a free OpenRouter key, this deck and the full script. I am happy to take questions, especially about client situations where you can't get a running legacy to compare against.

**Sources:** [README.md](README.md), [workshop-plan.md](workshop-plan.md)

---

## Likely audience questions & answers

Prepared answers. Same facts policy as the slides: stick to the repo; say "vendor claim" or "we did not test" where it applies.

**Q1. Isn't the diamond only possible for batch? What about CICS online transactions?**
Our harness is batch only; we have no CICS/BMS runtime ([comparison.md](comparison.md), limits). The idea carries over: capture inputs and outputs per transaction and compare. Google Dual Run supports batch as GA and online transactions in preview ✅ ([Dual Run overview](https://docs.cloud.google.com/mainframe-dual-run/docs/dual-run-overview)); Imogen verifies against captured production data flows ✅ ([Imogen](https://www.mechanical-orchard.com/platform)). For CICS the harness work is bigger and must be priced first.

**Q2. The client has no test LPAR and can't give us production data. What then?**
Then the first deliverable is the oracle. Options from our run: compile the unchanged COBOL with GnuCOBOL 3.2 (`-std=ibm -fsign=EBCDIC`) and shim LE services and VSAM, as we did for CBACT04C 🧪 ([workshop-plan.md](workshop-plan.md)), or a commercial runtime (Micro Focus/OpenText, Rocket 🟠). Generate synthetic scenarios rather than relying on samples (CardDemo's sample balances are all zero). Position: "if the legacy can't be run, price the harness work first" ([comparison.md](comparison.md)).

**Q3. Would a paid frontier model change the results?**
We did not test one; it is a listed stretch goal ([workshop-plan.md](workshop-plan.md)). Likely better recall on extraction. But the two missed rules (truncation, last account not posted) are behaviour, not text, and the grounded-but-wrong R17 shows that reading quality is not the limit. The diamond would still be required to know.

**Q4. Why Python and not Java in the workshop? Clients want Java.**
Speed of iteration and zero setup for a workshop. The diamond is language-agnostic: it compares records, not code. Porting the reference to Java/Spring behind the same diamond is a listed stretch goal ([workshop-plan.md](workshop-plan.md)).

**Q5. Is it legal / safe to send client COBOL to a cloud LLM?**
Depends on the contract. Options from comparison.md: IBM Bob for Z can be self-hosted on the customer's OpenShift with approved models ✅; Google MAT runs in the client's GCP project ✅; AWS Transform runs in AWS regions ✅; Microsoft's agents and an open workshop-style pipeline can use self-hosted models. EPAM MF Lens routes model calls through a LiteLLM proxy ✅ ([MF Lens docs](https://docs.codemie.ai/admin/deployment/extensions/mf-lens/)), so the model is configurable.

**Q6. Should we always replicate bugs bug-for-bug?**
No - but never fix silently. The diamond makes each deviation visible (fixing the last-account defect drops equivalence to 9/25 🧪), and the business decides per defect, in writing. Often: replicate first for a clean parallel run, then fix as a separate, tested change.

**Q7. How does this compare to just using AWS Transform since it's free now?**
For AWS-bound clients it is a sensible default ([comparison.md](comparison.md)). Free covers transformation; it does not give you the client-specific harness, scenario capture, SME rule verification, data migration and cutover. AWS itself points to partners (e.g. Imogen integration) for validation ✅/🟡. We did not run it ourselves.

**Q8. What about packed decimal (COMP-3) and EBCDIC? Your demo had none.**
Correct: CBACT04C in CardDemo uses ASCII extracts and no COMP-3 ([comparison.md](comparison.md), limits). We compile with `-fsign=EBCDIC` so sign handling follows IBM rules. A COMP-3 / EBCDIC primer is a planned backup slide ([talk-outline.md](talk-outline.md)); the diamond's per-field codec is where those encodings get decoded and compared.

**Q9. How long does it take to set up a harness like this for a real program?**
We only have our own number for one program: build ~1 s, one run ~20 ms, full diamond 0.5-0.7 s 🧪 - runtime, not effort. Effort depends on how many LE services, files and JCL features need shims; ex1's graph (copybooks, datasets, calls) is the input for that estimate. We have no verified effort benchmark across programs.

**Q10. Is "10,000 lines of verified code per engineer per week" realistic?**
It is Mechanical Orchard's own claim 🟡 ([Imogen Summer 2026](https://www.mechanical-orchard.com/insights/whats-new-in-imogen-the-summer-2026-release)), like their 11,578 LOC in 28 hours and EPAM's claimed 60% reverse-engineering savings. None is independently reproduced. Ask what "verified" means: which scenarios, which comparison schema.

**Q11. Does EPAM have a product in this space?**
Publicly, yes on the analysis side: MF Lens is EPAM IP inside AI/Run CodeMie for mainframe code analysis and exploration ✅, and it was named on the Q2 2026 call ✅. ISG's US 2026 mainframe report does not name EPAM among leaders ✅. Separately, the open part of the market for any services firm is still the verification harness and cutover — delivery-heavy work around whatever discovery tool is chosen.

**Q12. What about old Java/.NET - is AI more useful there?**
The gap between source and target is smaller, so deterministic recipes do most of the work: OpenRewrite/Moderne, GitHub Copilot modernization (uses OpenRewrite), AWS Transform for .NET ✅ ([comparison.md](comparison.md)). The model picks and composes recipes and fixes build errors; builds and tests are the check. We ran no workshop on it yet.
