# Comparison: AI-assisted legacy modernization offerings

Checked 2026-10-17. ✅ primary source, 🟡 vendor claim, 🟠 secondary only, ❌ not published / unknown. Sources in `research.md`.

## Mainframe (COBOL / PL/I) platforms

| | AWS Transform for mainframe | IBM Bob Premium Package for Z (ex watsonx Code Assistant for Z) | Google Cloud MAT + Dual Run | Microsoft Legacy-Modernization-Agents | Mechanical Orchard Imogen |
|---|---|---|---|---|---|
| Type | Managed agentic service ✅ | IDE agent + on-prem analysis ✅ | Self-deployed assessment tool (VM/GKE) + parallel-run service ✅ | Open-source sample framework ✅ | Platform + delivery team ✅ |
| Source languages | COBOL, PL/I, JCL, CICS, BMS, Db2, VSAM, IMS TM ✅ | COBOL, PL/I, Assembler, Java 🟠; CICS/IMS COBOL for optimize ✅ | Mainframe code (COBOL, JCL, ...) 🟠 exact list not read | COBOL (+ JCL in reverse engineering) ✅ | COBOL, JCL, PL/I; batch, transactions, screens 🟡 |
| Targets | Refactor: Java (deterministic, ex-Blu Age). Reimagine: any stack via Kiro/Claude Code (Java, Python, .NET...) ✅ | Java (COBOL/PL/I → Java), plus COBOL optimization in place ✅ | Code suggestions to Python, Java, C#, SQL ✅; actual transformation via partners 🟠 | Java Quarkus or C# .NET ✅ | Modern code (Java etc.) 🟡 |
| How it is checked | Deterministic refactor + human-in-the-loop; validation partly via partners (Imogen) ✅ | Generated unit tests for semantic equivalence ✅ | **Dual Run**: replay production, compare outputs (batch GA, online preview) ✅ | None built in (you add tests) ✅ | **Diamond / characterization tests against captured production data**, byte-level codecs ✅ |
| LLM | AWS-managed (Bedrock) 🟠 | IBM models + approved external models via Bob gateway ✅ | Gemini 2.5 Flash/Flash-Lite default, up to 3.1 Pro ✅ | Azure OpenAI, GitHub Copilot models, OpenAI ✅ | Multiple, not disclosed ❌ |
| Self-host / data residency | AWS regions only (18 regions for refactor) ✅ | **Yes**: self-hosted on customer OpenShift (Sep 2026) ✅ | Runs in your GCP project ✅ | Yes (your machine/Azure) ✅ | ❌ unknown |
| Pricing | Assessment + mainframe agent **free**; custom agent $0.035/agent-min; refactored runtime $0.31/core-h ✅ | Per authorized user + tokens (1 RU = 150k tokens ≈ 5-7k COBOL LOC) ✅; ~€1,454/user list 🟠 | ❌ contact sales; MAT consumes Vertex AI | Free (MIT/sample) + your LLM tokens 🟠 license not re-checked | ❌ engagement-based |
| Best for | AWS-bound clients, large estates, cheap start | IBM Z shops that stay on Z or move Java on Z; regulated, on-prem | GCP clients; assessment and *proof of equivalence* | PoCs, teaching, Azure clients | Risk-averse rewrites needing proof |

## Classic deterministic converters (pre-LLM, now adding AI on top)

| Vendor / tool | What | AI angle | Pricing |
|---|---|---|---|
| Heirloom Computing | COBOL→Java transpiler + runtime (CICS, JCL, VSAM, IMS) ✅ | Heirloom/X: AI refactoring after the deterministic baseline 🟡 | Subscription / per core, not public 🟠 |
| AWS Transform refactor (ex-Blu Age) | COBOL→Java, preserves architecture ✅ | Inside AWS Transform | Free transformation since Mar 2026 ✅ |
| TSRI JANUS Studio | Multi-language → Java/C#, microservice refactoring 🟠 | 🟠 | ❌ |
| Astadia CodeTurn / FastTrack | COBOL→Java/C# + test factory 🟠 | 🟠 | ❌ |
| CloudFrame | COBOL→Java cross-compilation; ISG Rising Star 🟠 | 🟠 | Pilot license up to 1.5M LOC; per converted LOC 🟠 |
| mLogica (via AWS) | Code conversion, e.g. Assembler→COBOL ✅ | - | $2.75 per LOC (Assembler→COBOL) ✅ |
| Rocket / OpenText (Micro Focus) | Replatform runtimes for COBOL off-mainframe 🟠 | 🟠 | ❌ |

## Open-source LLM pipeline (what we build in the workshop)

| Step | Tool | Deterministic? |
|---|---|---|
| Inventory + dependency graph (COBOL, copybooks, JCL, CICS) | regex/AST scanner (`ex1`), or tree-sitter/ProLeap COBOL parser | yes |
| Run the legacy as the oracle | GnuCOBOL 3.2 `-std=ibm -fsign=EBCDIC` + shims for LE services (CEE3ABD) and VSAM (indexed files) | yes |
| Business-rule extraction with citations | any LLM (free OpenRouter models), grounded by line ranges, scored against an answer key (`ex2`) | no → checked |
| New service | LLM from verified rules, or human (`ex3`) | no → checked |
| Proof | diamond / characterization tests, byte-level compare with a per-field schema (`ex4`) | yes |

Cost: $0 (free models, GnuCOBOL, CardDemo Apache-2.0). Limits: free models are slow (≈1-5 min per call) and rate-limited;
no CICS/BMS online runtime (batch only); no EBCDIC files or COMP-3 in this program (CardDemo ships ASCII extracts).

## Old Java / .NET

| | OpenRewrite / Moderne | GitHub Copilot modernization | AWS Transform for .NET / custom | IBM Bob (general) |
|---|---|---|---|---|
| Scope | Java 8→25, Spring, .NET Core 1→10, framework migrations ✅ | Java, .NET, C++ upgrades + Azure migration ✅ | .NET Framework → cross-platform .NET; custom agent for Java/Python/Node upgrades ✅ | 🟠 |
| Approach | Deterministic recipes; agent (Moddy / MCP) picks and composes them ✅ | Agent plans, uses OpenRewrite, builds, fixes CVEs, opens PR ✅ | Agent minutes; builds/tests used for validation ✅ | 🟠 |
| Price | OSS free; Moderne "$250K typical", "$2M typical" ✅ | Copilot licence 🟠 | .NET free within 50k agent-min/month; custom $0.035/agent-min ✅ | ❌ |

## How to position (for EPAM-style engagements)

- **Translation is commoditized** (free at AWS, bundled at IBM/Google). Differentiate on discovery quality, the
  equivalence harness, data migration and cutover - i.e. what MF Lens + delivery teams do.
- **Pick per client platform:** AWS → Transform (+ Imogen-style verification); IBM Z staying on Z → Bob for Z; GCP →
  MAT + Dual Run; multi-cloud/sovereign → open pipeline with self-hosted models (IBM self-hosted Bob is the only big-vendor option we found).
- **Always bring an oracle:** if the legacy can't be run (no test LPAR, no data), price the harness work first.
