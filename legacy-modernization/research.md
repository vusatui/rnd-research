# AI-assisted legacy modernization: research notes

Topic: AI-assisted modernization of legacy systems (COBOL/PL/I on mainframes, old Java/.NET), seen from the side of a
services company (EPAM-style): what clients are asking for, what the vendors sell, what actually works, and what we must
be able to demo.

All sources were checked on **2026-10-17** unless noted. Legend (same as the other topics):
- ✅ **verified**: read on the primary page (vendor docs, press release, paper, official filing/transcript).
- 🟡 **vendor-claim**: a vendor (or its customer story) talking about itself; not independently reproduced.
- 🟠 **secondary**: only from press/aggregators/partners; primary page not read by us.
- ❌ **unverified / conflicting**.
- 🧪 **measured by us** in the workshop (`workshop/`, CardDemo + GnuCOBOL + free OpenRouter models).

## TL;DR (key findings)

1. **Demand is real and is shifting from "convert code" to "understand + verify".** EPAM's own Q2 2026 call names AI-led
   mainframe modernization (with its MF Lens IP) as a driver of the fastest-growing vertical (financial services). Kyndryl
   (2,000 leaders, Oct 2026): only **9%** fully understand application dependencies; nearly half are behind schedule.
   ISG (Apr 2026): enterprises use GenAI to *extract and validate business rules* and prove functional equivalence through
   parallel testing.
2. **Code transformation is becoming free; verification is the product.** AWS made mainframe code transformation free
   (Mar 2026, replacing per-LOC pricing). The paid/defensible parts are discovery, equivalence testing (Google Dual Run,
   Mechanical Orchard Imogen, IBM's generated equivalence tests), runtimes and delivery. For a services company the value
   is the harness and the cutover, not the translation.
3. **Two technical schools, converging:** deterministic transpilers (Heirloom, AWS Transform *refactor* / ex-Blu Age,
   TSRI, Astadia, CloudFrame, mLogica) give provable but non-idiomatic code; LLM "reimagine" pipelines (AWS Transform
   *reimagine* + Kiro/Claude Code, Google MAT, IBM Bob for Z, Microsoft's open-source agents, Mechanical Orchard) give
   idiomatic code that must be proven. Everybody now pairs LLMs with deterministic analysis and an executable oracle.
4. **The failures live "below the business rules":** sign overpunch / packed decimal, VSAM key semantics, abend codes,
   uninitialized storage, truncation vs rounding. Our workshop reproduces exactly this class of bugs on AWS CardDemo 🧪.
5. **General LLMs read COBOL far better than they write it.** COBOL-Coder paper (2026): GPT-4o 97% compile / 85% pass@1
   COBOL→Java on single-file HumanEval-style tasks, but ~4% compile Java→COBOL; real systems need repository-level context.
6. **Our run (🧪):** with a *verified* rule list, a free model wrote a Python service that is byte-equivalent to the running
   COBOL on 25/25 scenarios; see `workshop-plan.md` for the LLM-extracted-rules and COBOL-only variants and the bugs the
   diamond caught.

## 1. Demand signals (why clients will ask)

| Claim | Status | Source |
|---|---|---|
| EPAM Q2 2026: financial services +11.5% YoY, fastest-growing vertical; driver incl. "mainframe modernization using EPAM IP to reverse engineer, automate and rebuild"; MF Lens named | ✅ (transcript) | [EPAM Q2 2026 call, Motley Fool transcript](https://www.fool.com/earnings/call-transcripts/2026/08/06/epam-epam-q2-2026-earnings-call-transcript/) |
| EPAM: wealth-management client, reverse engineering of >10M LOC, "60% time savings in reverse engineering effort" | 🟡 | same |
| EPAM: North American demand moving from task-based services (manual testing, front-end) to "AI-led modernization"; large pipeline deals incl. "legacy mainframe transformation", revenue expected H1 2027 | ✅ (statement) | same |
| EPAM's CEO: "Coding gets automated, engineering doesn't" | ✅ | same |
| EPAM MF Lens = "mainframe code analysis and exploration solution within the EPAM AI/Run platform"; enterprise feature; Neo4j + PostgreSQL + LiteLLM-proxied model, COBOL preprocessor | ✅ | [AI/Run CodeMie docs: MF Lens](https://docs.codemie.ai/admin/deployment/extensions/mf-lens/) |
| Kyndryl Modernization Report (Oct 1 2026, 2,000 leaders, 12 industries): nearly half behind schedule; 98% delayed modernization with negative impact; **9%** fully understand app dependencies; 25% have many undocumented apps; 10% use agentic AI in production for modernization (dependency mapping, code conversion, docs); 67% of those on/ahead of track vs 51% | ✅ (survey by a services vendor) | [Kyndryl press release](https://www.kyndryl.com/us/en/about-us/news/2026/10/enterprise-it-modernization-trends) |
| Kyndryl: "every organization with a mainframe now reports plans to deploy AI to the platform" - i.e. mainframes are not simply being retired | ✅ | same |
| ISG Provider Lens Mainframes US 2026 (Apr 17 2026): business-led modernization; GenAI to *extract and validate* rules, SMEs confirm logic, functional equivalence via parallel automated testing; 56 providers evaluated | ✅ | [ISG press release](https://ir.isg-one.com/news-market-information/press-releases/news-details/2026/U-S--Enterprises-Accelerate-Mainframe-Modernization/default.aspx) |
| ISG leaders include DXC, Kyndryl, TCS, Wipro, Capgemini, Cognizant, Infosys, HCLTech, Accenture, AWS, Google, Heirloom, mLogica, TSRI, Rocket... **EPAM is not named** in this US report | ✅ | same |
| GAO-25-107795 (Jul 2025): 11 critical federal legacy systems; 8 use outdated languages (e.g. COBOL, Assembly); 7 with known vulnerabilities; most agencies lack complete modernization plans | 🟠 (search summary of GAO page; report not read in full) | [GAO-25-107795](https://www.gao.gov/products/gao-25-107795) |
| Feb 23 2026 Anthropic article "COBOL modernization with AI: breaking the cost barrier": Claude Code automates exploration/analysis; "quarters instead of years"; COBOL ~95% of US ATM transactions | ✅ (article) / 🟡 (claims) | [claude.com article](https://claude.com/resources/articles/how-ai-helps-break-cost-barrier-cobol-modernization) |
| IBM shares fell 13.2% next day, biggest drop in 25+ years; IBM (Rob Thomas): "Translation captures almost none of the actual complexity" | 🟠 (ITPro citing Reuters; Reuters paywalled for us) | [ITPro](https://www.itpro.com/software/development/anthropic-says-claude-code-can-help-streamline-cost-prohibitive-cobol-modernization-but-ibm-says-its-not-that-simple-decades-of-hardware-software-integration-cannot-be-replicated-by-moving-code), [Reuters](https://www.reuters.com/business/ibm-posts-steepest-daily-drop-since-2000-after-anthropic-says-ai-can-modernize-2026-02-24/) |

**Takeaway for EPAM:** the client conversation is "we don't know what this does, prove the new thing does the same, and
don't stop the business". The deliverable that wins is discovery + equivalence evidence + incremental cutover.

## 2. Vendor landscape (details in `comparison.md`)

### AWS Transform for mainframe
| Claim | Status | Source |
|---|---|---|
| Supports z/OS COBOL and PL/I with JCL/PROC, CICS (CSD), BMS, Db2, VSAM, IMS TM; analysis, docs, business-logic extraction, decomposition, refactoring, IaC | ✅ | [AWS docs](https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe.html) |
| Three patterns in one service since Mar 17 2026: refactor (ex-Blu Insights / Blu Age, deterministic COBOL→Java), replatform, reimagine | ✅ | [AWS What's New, 2026-03-17](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-transform-mainframe-refactor/) |
| "Code transformation is now offered at no cost, replacing the previous lines-of-code based pricing model"; 3-level certification requirement removed | ✅ | same |
| Pricing page: assessment and mainframe modernization agent **free**; custom transformation agent **$0.035 / agent minute**; output infra billed normally | ✅ | [AWS Transform pricing](https://aws.amazon.com/transform/pricing/) |
| Refactored-app runtime: **$0.31 per AWS CPU core per hour** (or $0.155/vCPU on Fargate) | ✅ | [AWS Mainframe Modernization pricing](https://aws.amazon.com/mainframe-modernization/pricing/) |
| Reimagine: AWS Transform reverse-engineers rules, data lineage, dictionary; forward engineering with an agentic coder (Kiro, or Claude Code per AWS blog); targets Java, Python, .NET, ... | ✅ (AWS blog) | [AWS blog: reimagine with Claude Code](https://aws.amazon.com/blogs/migration-and-modernization/reimagining-mainframe-applications-with-aws-transform-and-claude-code/) |
| Also: AWS Transform for .NET (Framework → cross-platform .NET), free within 50k agent-minutes/month | ✅ | pricing page |

### IBM (watsonx Code Assistant for Z → IBM Bob Premium Package for Z)
| Claim | Status | Source |
|---|---|---|
| wca4z: discovery/analysis, refactoring, explanation, generation, COBOL→Java transformation with generated unit tests to compare semantic equivalence | ✅ (product page) / 🟡 (quality) | [IBM product page](https://www.ibm.com/products/watsonx-code-assistant-z) |
| 2.8.30+: COBOL→Java only via chat extension; 3-phase sub-session workflow for large COBOL/PL/I programs | ✅ | [What's new](https://www.ibm.com/docs/en/watsonx/watsonx-code-assistant-4z/2.x?topic=welcome-whats-new-in-watsonx-code-assistant-z) |
| Licensing: on-prem core by authorized user + virtual server; transformation/explanation/generation add-ons by tokens; 1 resource unit = 150k tokens ≈ 5,000-7,000 COBOL lines (20-30 tokens/line) | ✅ | [License guide](https://www.ibm.com/docs/en/watsonx/watsonx-code-assistant-4z/2.x?topic=information-license-guide-watsonx-code-assistant-z), [IBM Cloud doc](https://cloud.ibm.com/docs/watsonx-code-assistant?topic=watsonx-code-assistant-wcaz-tokenz) |
| Authorized-user subscription list price ~€1,454 net (Germany, Jan 2026) | 🟠 (IBM reseller page) | [Bücker GmbH](https://bueckergmbh.de/Kauf-IBM-D0GQ3ZX/IBM-watsonx-Code-Assistant-for-Z-for-IBM-Z-Authorized-User-Subscription-License) |
| IBM Bob Premium Package for Z (Sep 30 2026): agentic, IDE-based; deterministic app understanding + static analysis; **self-hosted on customer OpenShift** with approved models via Bob model gateway; Application View; zContext (curated Z knowledge); runtime-profiling-based COBOL performance hints | ✅ (announcement) | [IBM announcement 2026-09-30](https://www.ibm.com/new/announcements/ibm-bob-premium-package-for-z-expands-with-on-premises-deployment-and-new-saas-capabilities) |
| Bob for Z is the successor of wca4z | 🟠 (search summary; not stated explicitly on the page we read) | [IBM Bob for Z](https://www.ibm.com/products/ai-coding-agent/mainframe-modernization) |

### Google Cloud
| Claim | Status | Source |
|---|---|---|
| Mainframe Assessment Tool (MAT): Gemini-powered reverse engineering, rules, docs, dependencies, test cases; deploy as VM or on GKE in your project | ✅ | [MAT setup docs](https://docs.cloud.google.com/mainframe-assessment-tool/docs/create-instance), [solution page](https://cloud.google.com/solutions/mainframe-modernization) |
| MAT default models Gemini 2.5 Flash-Lite/Flash; options up to Gemini 3.1 Pro (preview); can emit code suggestions to Python, Java, C#, SQL; generated test cases | ✅ | [MAT settings](https://docs.cloud.google.com/mainframe-assessment-tool/docs/configure-settings) |
| MAT exposes an MCP server (`MAT_ENABLE_MCP=true`) for agents | ✅ | [MAT MCP](https://docs.cloud.google.com/mainframe-assessment-tool/docs/mcp-server) |
| Dual Run: run mainframe and Google Cloud side by side, compare outputs, replay production events; batch GA, online transactions preview | ✅ | [Dual Run overview](https://docs.cloud.google.com/mainframe-dual-run/docs/dual-run-overview) |
| Pricing for MAT / Dual Run | ❌ not published (contact sales; MAT uses your Vertex AI quota) | - |

### Microsoft / GitHub
| Claim | Status | Source |
|---|---|---|
| Azure-Samples **Legacy-Modernization-Agents** (open source): COBOL → Java Quarkus or C# .NET; Microsoft Agent Framework; Azure OpenAI, GitHub Copilot SDK or OpenAI; reverse-engineering + conversion + dependency mapping + portal | ✅ (README via search) | [GitHub repo](https://github.com/Azure-Samples/Legacy-Modernization-Agents), [MS dev blog](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/) |
| MS dev blog admits early GPT-4 attempts produced "a good mix of educated guesses ... and hallucinational gibberish" | ✅ | same blog |
| GitHub Copilot modernization: Java, .NET, C++ assessment/upgrade/Azure migration (uses OpenRewrite); GA for IDE; not COBOL | ✅ | [Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/github-copilot-app-modernization/overview) |

### Specialists and classic converters
| Claim | Status | Source |
|---|---|---|
| Mechanical Orchard Imogen: behaviour-based rewrite, verifies new code against captured production data flows, slice by slice; integrates AWS Transform and Google MAT | ✅ (vendor page) | [Imogen platform](https://www.mechanical-orchard.com/platform) |
| Imogen Summer 2026: AWS Transform rules integration, autonomous build+verify pipeline ("software dark factory"); ">10,000 lines of verified code per engineer per week"; Leidos partnership | 🟡 | [Summer 2026 release](https://www.mechanical-orchard.com/insights/whats-new-in-imogen-the-summer-2026-release) |
| MO record: 11,578 LOC in 28 hours at a F100 retailer, "fully verified" | 🟡 | [First year of Imogen](https://www.mechanical-orchard.com/insights/reflections-on-the-first-year-of-imogen) |
| MO field CTO (Jun 2026), on **AWS CardDemo**: LLM-only Java replica compiled and ran but treated KSDS as flat file, emitted negatives as "-" strings instead of overpunch, dropped a COBDATFT branch, replaced abend 999 with exit 12; argues for the "diamond" (same input to COBOL and new code, byte compare) | ✅ (article) / 🟡 (their experiment) | [Modernization is a verification problem](https://www.mechanical-orchard.com/research/mainframe-modernization-is-a-verification-problem) |
| Heirloom: deterministic COBOL→Java transpiler ("compiles, not translates") + runtime for CICS/JCL/VSAM/IMS; argues LLMs belong on docs, tests, refactoring after a deterministic baseline; claims PHEAA as largest mainframe-to-AWS migration | ✅ (article) / 🟡 (claims) | [Heirloom: LLMs and COBOL](https://heirloomcomputing.com/llms-and-cobol-modernization/) |
| TSRI JANUS Studio, Astadia CodeTurn, CloudFrame, mLogica (AWS code conversion, e.g. Assembler→COBOL $2.75/LOC), Raincode compilers | 🟠 / ✅ for mLogica price (AWS pricing page) | [TSRI](https://tsri.com/cobol-modernization/), [Astadia](https://www.astadia.com/products/codeturn), [CloudFrame](https://cloudframe.com/CodeNavigator), [AWS pricing](https://aws.amazon.com/mainframe-modernization/pricing/) |
| Old Java/.NET: OpenRewrite (open source, deterministic recipes) / Moderne (commercial, Moddy agent; "$250K typical", "$2M typical" enterprise) | ✅ | [Moderne pricing](https://moderne.ai/pricing), [OpenRewrite](https://moderne.ai/openrewrite) |

## 3. Evidence on LLM quality

| Claim | Status | Source |
|---|---|---|
| COBOL-Coder (Concordia + FPT, arXiv 2604.03986): on COBOLEval GPT-4o 41.8% compile / 16.4 pass@1; COBOL-Coder-14B 73.95% / 49.33; most open models 0% | ✅ (paper) | [arXiv 2604.03986](https://arxiv.org/abs/2604.03986) |
| COBOL→Java (COBOL-JavaTrans, 143 HumanEval-style pairs): GPT-4o 97.2% compile / 85.3 pass@1; gpt-oss-120B 98.6 / 89.5; Java→COBOL: GPT-4o 4.4% / 2.2 | ✅ | same |
| Authors: single-file benchmark, no copybooks/JCL/cross-program deps; practitioners see LLMs as "junior developer drafts"; restartability, file status, SQLCODE handling are adoption requirements | ✅ | same |
| IBM research on automated validation/testing of COBOL→Java transformation (ASE 2024, FSE 2025) | 🟠 (abstract-level) | [arXiv 2506.10999](https://arxiv.org/abs/2506.10999) |

Read: LLMs are good *readers* of COBOL (explain, extract, translate small units into Java) and poor *writers* of COBOL;
benchmarks say nothing about system-level behaviour (files, encodings, JCL, restart), which is where projects fail.

## 4. What we reproduced ourselves (🧪, 2026-10-17)

Setup: [AWS CardDemo](https://github.com/aws-samples/aws-mainframe-modernization-carddemo) (Apache-2.0, commit
`59cc6c2`, 31 COBOL programs ≈ 20.6k lines, 38 JCL), program **CBACT04C** (interest calculation batch, 652 lines),
compiled *unchanged* with GnuCOBOL 3.2 (`-std=ibm -fsign=EBCDIC`), VSAM KSDS emulated with GnuCOBOL indexed files,
`CEE3ABD` and JCL `PARM` shimmed. Full numbers in `workshop-plan.md`.

- Deterministic dependency graph of the whole CardDemo tree in <1 s (157 nodes, 385 edges); 16 online programs have
  dynamic `XCTL PROGRAM(var)` targets static analysis cannot resolve - exactly the "only 9% know their dependencies" gap.
- Found while building the harness (all "below the business rules"):
  - Abend 999 becomes **exit status 231** on Linux (999 mod 256) - an operator watching for 999 sees nothing.
  - The transaction description is built with `STRING ... INTO` and keeps **LOW-VALUES** (x'00') instead of spaces in
    the rest of the 100-byte field: byte-exact comparison fails until the comparison schema says how to treat it.
  - Latent defect: the **last account's interest is never posted** to its balance (loop exits at EOF before the control
    break). Interest transactions are written, balance is not. A "clean" re-implementation fails equivalence on 16/25
    scenarios - the business must decide: replicate the bug or fix it consciously.
  - CardDemo's sample category balances are all zero, so "it matches on the sample data" proves nothing; generated
    scenarios are required.
  - Our own REST API first returned money as JSON floats and **`-0.0`** for a truncated negative cent: the legacy record
    has no negative zero. Caught by a test, fixed.
- LLM results (free OpenRouter models): see `workshop-plan.md` - verified rules → equivalent code; the diamond is what
  tells the three variants apart.

## 5. Open items / unverified

- Pricing for Google MAT/Dual Run, IBM Bob for Z, Mechanical Orchard, Heirloom, TSRI, CloudFrame: not public (❌).
- IBM share drop figures read only via ITPro (Reuters paywalled); GAO report read only via summary (🟠).
- All productivity numbers (EPAM 60%, MO 10k LOC/week, AWS "years to months") are vendor claims (🟡).
- We did not run AWS Transform, MAT, Bob or Imogen (all need accounts/contracts); comparison is from docs.
- Old Java/.NET part is lighter: we covered tooling (OpenRewrite/Moderne, Copilot modernization, AWS Transform .NET) but
  ran no workshop on it. Candidate follow-up: Java 8 → 21 / .NET Framework → .NET 8 with OpenRewrite + an LLM, same diamond idea.
