# Workshop: modernize a real mainframe batch job and prove it is equivalent

See [`../workshop-plan.md`](../workshop-plan.md) for the agenda, step-by-step commands and our measured results.

```
setup.sh                    fetch AWS CardDemo (Apache-2.0) at a pinned commit into vendor/ (git-ignored), check GnuCOBOL
legacy/                     build.sh + run_legacy.py: CBACT04C compiled UNCHANGED with GnuCOBOL, VSAM/JCL/LE shims
common/                     OpenRouter client (free models, fallback, JSON extraction), fixed-width record codec
ex1_dependency_graph/       deterministic graph of the whole CardDemo tree (+ optional grounded LLM summary)
ex2_rule_extraction/        LLM extracts business rules with line citations; grounding check + score vs answer key
ex3_new_service/            contract, reference implementation, FastAPI service, LLM generator (from rules or from COBOL)
ex4_equivalence/            the "diamond": same inputs to COBOL and to the new code, byte-level compare
tests/                      offline pytest suite (no LLM, no network)
out/                        generated artifacts (git-ignored)
```
