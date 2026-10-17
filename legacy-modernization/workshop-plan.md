# Workshop plan (~100 min): modernize a mainframe batch job with AI - and prove it

Everything is free: GnuCOBOL 3.2, AWS CardDemo (Apache-2.0), Python 3.10+, a free OpenRouter key. Code: [`workshop/`](workshop/).
Subject: **CBACT04C**, CardDemo's monthly interest-calculation batch job (652 lines COBOL, 5 copybooks, run by JCL `INTCALC`).

| # | Time | Exercise | Needs | What participants do / learn |
|---|---|---|---|---|
| 0 | 10 min | Setup | GnuCOBOL, Python | `./setup.sh`, venv, `./legacy/build.sh`, `python legacy/run_legacy.py`: the *unchanged* COBOL runs locally with VSAM (indexed files), JCL PARM and `CEE3ABD` shims. `pytest -q tests` |
| 1 | 15 min | **Dependency graph** (`ex1_dependency_graph/graph.py`) | none | Deterministic inventory of the whole tree (programs, copybooks, JCL jobs, datasets, CICS files). `--impact ACCTDATA`: who writes the account master? `--focus CBACT04C` → Mermaid. Optional `--explain`: LLM summary grounded in the edges. Lesson: do discovery deterministically, let the LLM explain it |
| 2 | 25 min | **Business-rule extraction** (`ex2_rule_extraction/extract.py --runs 3`) | OpenRouter key | LLM returns rules with line citations. Two checks: *grounding* (do cited lines exist and contain the symbols?) and *recall vs a hand-verified answer key* (`gold_rules.json`, 15 rules incl. polarity checks). Drift across runs. Lesson: grounded ≠ correct |
| 3 | 20 min | **New service** (`ex3_new_service/`) | OpenRouter key (generator) | Contract + reference implementation + FastAPI (`uvicorn ex3_new_service.api:app`). Generate candidates with an LLM three ways: from verified rules, from the LLM's own rules (`--rules out/rules.json`), from COBOL only (`--from-cobol`) |
| 4 | 25 min | **Diamond equivalence** (`ex4_equivalence/diamond.py`) | none | Same inputs → running COBOL and new code → byte-level compare (timestamps masked, FILLER ignored, `--strict` for byte-exact). 25 scenarios: CardDemo data, edge amounts, 20 generated, 2 abend paths. Run every candidate; run `--fixed` to see what "fixing the bug" costs |
| - | 5 min | Wrap-up | | Map the four steps to AWS Transform / IBM Bob / Google MAT + Dual Run / Imogen (`comparison.md`) |

Stretch goals: add a scenario that breaks the reference (e.g. an account whose group has no category rows); handle
`--strict` LOW-VALUES properly; port the reference to Java/Spring and keep the same diamond; add a second program
(`CBTRN02C`, transaction posting) to the harness; try a paid model and compare recall/equivalence.

## Commands

```bash
cd legacy-modernization/workshop
./setup.sh && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./legacy/build.sh && python legacy/run_legacy.py
python -m pytest -q tests
python ex1_dependency_graph/graph.py --focus CBACT04C --impact ACCTDATA
export OPENROUTER_API_KEY=...            # or put it in workshop/.env (see .env.example); never commit it
python ex2_rule_extraction/extract.py --runs 3
python ex3_new_service/generate.py                          # from verified rules
python ex3_new_service/generate.py --rules out/rules.json --out out/candidate_rules.py
python ex3_new_service/generate.py --from-cobol --out out/candidate_cobol.py
python ex4_equivalence/diamond.py                            # reference
python ex4_equivalence/diamond.py --fixed                    # reference with the defect fixed
python ex4_equivalence/diamond.py --impl out/candidate_llm.py   # and the other candidates
```

## Measured results (2026-10-17, our box, free OpenRouter models, reasoning off)

**Harness and deterministic parts**
- Build of CBACT04C + shims with GnuCOBOL 3.2: ~1 s. One legacy run incl. loading 4 KSDS files: ~20 ms; full diamond (25 scenarios, both sides): **0.5-0.7 s**.
- ex1 over the whole CardDemo tree (31 programs, 38 JCL, 46 copybooks): 157 nodes / 385 edges in <1 s; 16 programs have dynamic `XCTL PROGRAM(var)` targets that static analysis can't resolve.
- `pytest`: 9 passed, <1 s.

**ex2 - rule extraction (CBACT04C + copybooks, ~40k chars prompt)**

| Model | Runs | Time / run | Rules | Ungrounded | Recall vs answer key | Always missed |
|---|---|---|---|---|---|---|
| `nvidia/nemotron-3-super-120b-a12b:free` | 4 | 78-163 s (one retry on broken JSON) | 25-43 | 0-9 | 0.60-0.73 | TRUNCATION, NEGATIVE_BALANCE, LAST_ACCOUNT_NOT_POSTED |
| `poolside/laguna-s-2.1:free` | 1 | 55 s | 20 | 1 | 0.87 | TRUNCATION, LAST_ACCOUNT_NOT_POSTED |

Drift across 3 nemotron runs (1 - Jaccard of covered gold rules): **0.25** (FEES_STUB, RESET_CYCLE, ZERO_RATE_SKIP flip).
No run found the two rules that matter most for money: **truncation instead of rounding** and the **last account never
being posted**. One run produced a rule that is *grounded* (right lines, right symbols) and *wrong*:
> R17 [219-221] "When END-OF-FILE is 'Y' (after loop exit), the program performs 1050-UPDATE-ACCOUNT to persist the last account's accumulated interest."

The code reads like that, but the `ELSE` branch is unreachable: the loop exits first. Our first keyword scorer counted
such rules as hits; the answer key now has polarity checks (`require_any`), which is itself a lesson about LLM-as-judge.

**ex3 + ex4 - candidates through the diamond (25 scenarios)**

| Candidate | Generator | Equivalent | What the diamond caught |
|---|---|---|---|
| Hand-written reference (`interest.py`) | - | **25/25** | - |
| Reference with the defect fixed (`--fixed`) | - | 9/25 | last account's balance now gets interest: a business decision, not a bug fix by default |
| LLM from **verified** rules (3 runs) | nemotron-3-super | **25/25, 25/25, 25/25** (12-85 s) | - |
| LLM from **LLM-extracted** rules (3 rule sets) | nemotron-3-super | **2/25, 1/25, 0/25** | abends where legacy falls back to `DEFAULT` rate; rate looked up only once per account; interest posted for the last account; tx id format; `UnboundLocalError` crash in one candidate |
| LLM from **COBOL only**, no rules (3 runs) | gemma-4-31b, nemotron-3-super ×2 | **1/25, 3/25, 2/25** | `ROUND_HALF_UP` instead of truncation (12.49 vs 12.50), last account posted, missing abends (`.get()` instead of abend 999), transaction order/count |

Takeaways: (1) the LLM is a good *implementer* of a correct spec and a mediocre *extractor* of the spec; (2) "LLM reads
COBOL, LLM writes Java" fails on exactly the money-relevant details; (3) only the running COBOL told us which candidate is
right - code review of the 70-100-line candidates would have missed most of these.

**Harness findings (below the business rules)**: abend 999 shows up as process exit 231; the `STRING ... INTO` target
keeps LOW-VALUES (x'00') - byte-exact `--strict` mode fails 6/8 scenarios on `TRAN-DESC` until the comparison schema
decides; CardDemo's sample balances are all zero (sample-data scenario passes for almost any candidate); our own API
initially leaked `-0.0` and floats for money.

## Facilitator notes
- Free models are slow and rate-limited (we saw 429s on gemma); `common/llm.py` falls through a model list. Turn hidden
  reasoning off (`OPENROUTER_REASONING=off`, default): with reasoning on, nemotron spent >5 min and returned truncated/empty JSON.
- Keep pre-generated `out/` artifacts on a USB stick / branch as a fallback for the live demo.
- GnuCOBOL must have an indexed-file handler (BDB or VBISAM): `cobc --info | grep -i indexed`.
