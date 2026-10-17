# Talk outline (~35 min): "AI won't translate your COBOL for you - but it will help you prove the new system is right"

Audience: engineers, architects, pre-sales at a services company. Goal: understand why clients are coming *now*, what the
vendors really sell, where AI helps and where it silently breaks things, and how we de-risk an engagement.

| # | Min | Section | Content | Visual / demo |
|---|---|---|---|---|
| 1 | 0-3 | Hook | Feb 23 2026: an Anthropic article on COBOL modernization, next day IBM -13% (🟠). In Mar 2026 AWS made mainframe code transformation free. Question: if translation is free, what are clients paying for? | Two headlines side by side |
| 2 | 3-7 | Why now (demand) | EPAM Q2 2026: AI-led mainframe modernization drives FS growth; Kyndryl: 9% understand dependencies, ~half behind schedule; ISG: "extract and validate rules, prove equivalence by parallel testing"; GAO federal systems. Talent cliff + AI on the mainframe, not just off it | 3 numbers slide |
| 3 | 7-11 | What "legacy" actually is | COBOL program ≠ system: JCL, copybooks, VSAM KSDS, CICS/BMS, Db2, assembler helpers, LE services, schedulers. Four strategies: rehost / refactor / rewrite(reimagine) / replace | CardDemo dependency graph from ex1 (157 nodes, 385 edges) |
| 4 | 11-15 | Where AI is good | Reading & explaining, dependency/impact analysis (with a deterministic graph), rule extraction with citations, test generation, forward engineering of *small, specified* units. COBOL-Coder numbers: GPT-4o 97% compile on COBOL→Java, ~4% on Java→COBOL | Table: read vs write |
| 5 | 15-20 | Where it breaks: "below the business rules" | Sign overpunch / packed decimal, truncation vs rounding, KSDS key semantics, LOW-VALUES in STRING targets, abend 999 → exit 231, latent defects that the business relies on. MO's CardDemo READACCT story (🟡) + our CBACT04C findings (🧪) | Byte dump of a TRAN-RECORD, legacy vs modern |
| 6 | 20-23 | The diamond | Same input → running COBOL (oracle) and new code → byte compare with a per-field schema. Characterization tests, generated scenarios (sample data is all zeros!). Google Dual Run and Imogen are productized diamonds | Diamond diagram |
| 7 | 23-29 | Live demo | ex1 graph → ex2 LLM extracts rules (grounding + recall vs answer key) → ex3 three candidates: verified rules / LLM rules / COBOL-only → ex4 diamond: 25/25 vs ... vs 1/25 (rounding + last-account bug + missing abends) | Terminal; backup: recorded output in `workshop-plan.md` |
| 8 | 29-32 | Vendor map | AWS Transform (free, refactor+reimagine), IBM Bob for Z (self-hosted, stays on Z), Google MAT + Dual Run, Microsoft open-source agents, Mechanical Orchard, deterministic transpilers (Heirloom & co), Moderne/OpenRewrite for old Java/.NET. Translation commoditized → value in discovery + verification + cutover | `comparison.md` table |
| 9 | 32-35 | How we run an engagement + Q&A | 1) inventory & graph, 2) get the oracle running (test LPAR or GnuCOBOL/Micro Focus harness), 3) capture production-like inputs, 4) extract & verify rules with SMEs, 5) generate code per slice, 6) diamond in CI, 7) strangler cutover with parallel run. Decide bug-for-bug vs fix explicitly | Checklist slide |

Key messages to repeat: *the running legacy is the spec*; *trust the harness, not the model's account of what it did*;
*free translation makes verification the product*.

Backup slides: COMP-3 / EBCDIC primer; KSDS vs flat file; costs (AWS free / $0.035 agent-min / $0.31 core-h; IBM 150k
tokens ≈ 5-7k LOC); old Java/.NET with OpenRewrite recipes + LLM.
