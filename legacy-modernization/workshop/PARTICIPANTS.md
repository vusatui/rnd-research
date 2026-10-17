# Participant guide: modernize a mainframe batch job with AI - and prove it

You will take **CBACT04C**, the monthly interest-calculation batch job from AWS CardDemo (real, unchanged COBOL),
run it locally, extract its business rules with a free LLM, generate a new Python service, and prove (or disprove)
that the new code behaves exactly like the COBOL.

Everything is free. Time: ~100 min. Facilitator agenda: [`../workshop-plan.md`](../workshop-plan.md).

> All outputs below come from a clean clone run on 2026-10-17 (Linux, GnuCOBOL 3.2, Python 3.12, free OpenRouter
> models). LLM outputs will differ on your machine; that is part of the lesson.

## 1. Prerequisites

| What | Version | Check |
|---|---|---|
| git | any | `git --version` |
| Python | 3.10+ | `python3 --version` |
| GnuCOBOL | 3.x **with an indexed-file handler** (BDB or VBISAM) | `cobc --version`, `cobc --info \| grep -i indexed` |
| OpenRouter key | free account | needed only for ex2, ex3 generator, ex1 `--explain` |

### Install GnuCOBOL

- **Ubuntu / Debian / WSL2 (Ubuntu):** `sudo apt-get update && sudo apt-get install -y gnucobol3` (older releases: `gnucobol`)
- **Fedora:** `sudo dnf install gnucobol`
- **macOS (Homebrew):** `brew install gnucobol`
- **Windows:** use WSL2 with Ubuntu (`wsl --install -d Ubuntu`), then follow the Ubuntu line. Native Windows builds are not supported by this workshop.

Verify the indexed-file handler - CBACT04C reads VSAM KSDS files, emulated as indexed files:

```
$ cobc --info | grep -i "indexed file handler"
indexed file handler     : BDB
```

If it says `disabled`, your GnuCOBOL build cannot run the job; install a distro/Homebrew package instead of a minimal build.

### Get a free OpenRouter key

1. Sign up at <https://openrouter.ai>, open <https://openrouter.ai/keys>, create a key. No credit card is needed for `:free` models.
2. **Use free models only** (ids ending in `:free`). The code defaults to a list of free models and never needs a paid one.
3. Never commit the key. It goes into `workshop/.env`, which is git-ignored.

## 2. Setup (10 min)

```bash
git clone https://github.com/vusatui/rnd-research.git
cd rnd-research/legacy-modernization/workshop
./setup.sh                                   # clones AWS CardDemo at a pinned commit into vendor/, checks the toolchain
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                         # then put your key into OPENROUTER_API_KEY=
./legacy/build.sh                            # compiles the UNCHANGED CBACT04C + shims
python legacy/run_legacy.py                  # runs the COBOL job on CardDemo sample data
python -m pytest -q tests                    # offline checks, no LLM
```

Expected:

```
CardDemo at 59cc6c2 -> .../workshop/vendor/carddemo
cobc (GnuCOBOL) 3.2.0
indexed file handler     : BDB
OK. Next: python -m pip install -r requirements.txt
built: CBACT04C.so CEE3ABD.so dumpacct loadksds runparm
RC 0 | transactions: 50 | accounts: 50
...
DISCLOSURE GROUP RECORD MISSING
TRY WITH DEFAULT GROUP CODE
END OF EXECUTION OF PROGRAM CBACT04C
9 passed in 0.83s
```

`.env` options (see `.env.example`):

| Variable | Meaning |
|---|---|
| `OPENROUTER_API_KEY` | your key (required for LLM steps) |
| `OPENROUTER_MODEL` | optional: pin one free model; otherwise the fallback list in `common/llm.py` is used |
| `OPENROUTER_REASONING` | `off` (default). Hidden reasoning makes free models slow and can truncate answers |
| `LLM_DEBUG=1` | (env) print model, latency and failures for every call |

**What to observe:** a 1980s-style mainframe job runs on your laptop in ~20 ms. The "DISCLOSURE GROUP RECORD MISSING /
TRY WITH DEFAULT GROUP CODE" lines are the program's own DISPLAY output: a fallback rule, in the code, that nobody documented.

## 3. Exercise 1 - Dependency graph (15 min, no LLM)

**Goal:** discover what CBACT04C touches and who else writes the same data - deterministically.

```bash
python ex1_dependency_graph/graph.py --focus CBACT04C --impact ACCTDATA
```

Expected (abridged):

```
nodes: {'dataset': 30, 'program': 30, 'external': 5, 'copybook': 46, 'utility': 8, 'job': 38}
edges: {'reads': 42, 'writes': 21, 'call': 17, 'copies': 208, 'updates': 3, 'dd-only': 5, 'xctl': 3, 'uses': 31, 'runs': 55}
programs with unresolved dynamic XCTL/LINK targets: 16 -> COACTUPC, COACTVWC, COADM01C, ...
impact analysis for dataset ACCTDATA:
  CBACT01C   reads    (batch, via JOB:READACCT)
  CBACT04C   updates  (batch, via JOB:INTCALC)
  CBTRN02C   updates  (batch, via JOB:POSTTRAN)
  ...
CBACT04C: 13 edges -> out/CBACT04C.mmd
graph LR
  CBACT04C["CBACT04C"] -->|updates| ACCTDATA["ACCTDATA"]
  ...
```

Paste `out/CBACT04C.mmd` into <https://mermaid.live> to see the picture. Optional: `python ex1_dependency_graph/graph.py --focus CBACT04C --explain` asks an LLM to summarize **only** the edges it is given.

**What to observe:**
- Two batch jobs update the account master (INTCALC and POSTTRAN): you cannot migrate CBACT04C alone without deciding about CBTRN02C.
- 16 online programs have dynamic `XCTL PROGRAM(variable)` targets - static analysis (and an LLM reading the code) cannot resolve them; you need runtime data.
- Lesson: do discovery with a parser, use the LLM to explain it.

**Stretch:** run `--impact TRANSACT` or `--focus CBTRN02C`; find a dataset that is written but never read.

## 4. Exercise 2 - Business-rule extraction (25 min, LLM)

**Goal:** have an LLM extract business rules with line citations, then check them two ways: *grounding* (do the
cited lines contain the symbols?) and *recall* against a hand-verified answer key (`ex2_rule_extraction/gold_rules.json`, 15 rules).

```bash
LLM_DEBUG=1 python ex2_rule_extraction/extract.py              # 1 run, ~1-3 min on free models
python ex2_rule_extraction/extract.py --runs 3                 # drift across runs (longer)
python ex2_rule_extraction/extract.py --rescore                # re-score out/rules.json, no LLM call
```

Expected (our run; numbers will vary):

```
  [nvidia/nemotron-3-super-120b-a12b:free] 132s finish=stop chars=18542
run 1: nvidia/nemotron-3-super-120b-a12b:free | 132.2s | 41 rules | ungrounded 5 | recall vs answer key 0.73 | missed: ZERO_RATE_SKIP, TRUNCATION, NEGATIVE_BALANCE, LAST_ACCOUNT_NOT_POSTED
   ungrounded R2: none of ['TCATBAL-FILE', 'XREF-FILE', 'DISCGRP-FILE', 'ACCOUNT-FILE'] appear in cited lines
   ...
wrote out/rules.json and out/rules_report.json
```

**What to observe:**
- Recall is typically 0.6-0.87. Look at what is *missed*: `TRUNCATION` (interest is truncated, not rounded) and
  `LAST_ACCOUNT_NOT_POSTED` (the last account's interest is never written back - a real defect in the COBOL). These are exactly the money-relevant rules.
- Read `out/rules.json`: find a rule that is grounded (right lines, right symbols) and still wrong. Grounded is not correct.
- With `--runs 3`, watch which rules flip between runs (drift).

## 5. Exercise 3 - The new service (20 min, LLM for the generator)

**Goal:** see the target: a contract, a hand-written reference implementation, a REST API - and LLM-generated candidates.

```bash
uvicorn ex3_new_service.api:app --port 8000        # in a second terminal; open http://localhost:8000/docs
curl -s -X POST localhost:8000/interest-runs -H 'content-type: application/json' -d '{
  "run_date":"2026-10-17",
  "accounts":[{"acct_id":"00000000001","curr_bal":"1000.00","group_id":"A000000000"}],
  "card_by_account":{"00000000001":"4111111111111111"},
  "rates":[{"group_id":"A000000000","type_cd":"01","cat_cd":"0001","rate":"15.00"}],
  "balances":[{"acct_id":"00000000001","type_cd":"01","cat_cd":"0001","balance":"1000.00"}]}'
```

Expected:

```
{"transactions":[{"tran_id":"2026-10-17000001","type_cd":"01","cat_cd":"0005","source":"System","desc":"Int. for a/c 00000000001","amount":"12.50","card_num":"4111111111111111"}],"accounts":[{"acct_id":"00000000001","curr_bal":"1000.00","curr_cyc_credit":"0.00","curr_cyc_debit":"0.00"}]}
```

Note `curr_bal` stays `1000.00`: a 12.50 interest transaction is written, but the (last) account is not updated. That is the legacy behaviour, faithfully reproduced.

Generate candidates three ways (each ~10-90 s):

```bash
python ex3_new_service/generate.py                                                     # from VERIFIED rules -> out/candidate_llm.py
python ex3_new_service/generate.py --rules out/rules.json --out out/candidate_rules.py  # from the LLM's own rules (ex2)
python ex3_new_service/generate.py --from-cobol --out out/candidate_cobol.py           # from COBOL only
```

Expected: `nvidia/nemotron-3-super-120b-a12b:free: 71 lines in 12s -> .../out/candidate_llm.py`

**What to observe:** read a candidate (~70-100 lines). Does it look right? Write down your guess before ex4.

## 6. Exercise 4 - Diamond equivalence (25 min, no LLM)

**Goal:** feed the same inputs to the running COBOL and to the new code, compare outputs field by field (timestamps masked, FILLER ignored).

```bash
python ex4_equivalence/diamond.py                                 # the reference implementation
python ex4_equivalence/diamond.py --fixed                         # reference with the defect "fixed"
python ex4_equivalence/diamond.py --strict                        # byte-exact, no normalisation
python ex4_equivalence/diamond.py --impl out/candidate_llm.py     # each of your candidates
```

Expected:

```
carddemo-sample-data           legacy ok                   tx=50  EQUIVALENT
edge-amounts                   legacy ok                   tx=9   EQUIVALENT
...
abend-missing-default-rate     legacy abend 999 (exit 231) tx=1   EQUIVALENT
abend-unknown-account          legacy abend 999 (exit 231) tx=1   EQUIVALENT
25/25 scenarios equivalent in 0.5s
```

`--fixed` -> `9/25` (e.g. `acct 00000000035 curr_bal: legacy=Decimal('166.00') modern=Decimal('2127.30')`).
`--strict` -> `2/25` (the COBOL leaves LOW-VALUES `x'00'` in `TRAN-DESC`).

LLM candidates: in our earlier runs, candidates from verified rules scored 25/25 three times, from LLM-extracted rules
0-2/25, from COBOL only 1-3/25. In the clean-clone verification run, two fresh candidates from **verified** rules scored
**2/25**: the model wrote `'Int. for/a/c ...'` instead of `'Int. for a/c ...'` - one character, every transaction.

**What to observe:**
- Fixing a bug is a behaviour change: `--fixed` breaks 16 scenarios. It is a business decision, not a refactoring.
- Each DIFF line tells you the field and both values; compare with your guess from ex3.
- Only the running COBOL could tell us which candidate is right. Code review of 70 lines would miss most of this.

**Stretch tasks**
- Add a scenario in `ex4_equivalence/scenarios.py` that breaks the reference (e.g. a group with no category rows).
- Make `--strict` pass by deciding how to treat LOW-VALUES in the comparison schema.
- Port `interest.py` to Java/Spring and keep the same diamond (adapter in `ex4_equivalence/adapter.py`).
- Add `CBTRN02C` (transaction posting) to the harness.
- Feed the DIFF lines back to the generator and loop until 25/25; count iterations.
- Try a different free model (`OPENROUTER_MODEL=...`) and compare recall and equivalence.

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `GnuCOBOL missing` from `setup.sh` | install it (section 1); reopen the shell |
| `indexed file handler: disabled` / file status 30/37 on run | GnuCOBOL built without BDB/VBISAM; use the distro/Homebrew package |
| `Warning: program compiled against libxml ...` | harmless |
| `Set OPENROUTER_API_KEY` | `cp .env.example .env` and fill the key, or `export OPENROUTER_API_KEY=...` |
| Slow (1-3 min per call) | normal for free models on a 40k-char prompt. Keep `OPENROUTER_REASONING=off` |
| 429 / rate limited, empty reply, broken JSON | `common/llm.py` retries twice per model and falls through the free-model list automatically. Set `LLM_DEBUG=1` to watch. If all fail, wait a minute or pin another model |
| A model id no longer exists | free models change often: `python list_free_models.py`, then set `OPENROUTER_MODEL` |
| Free-tier daily limit hit | use the facilitator's pre-generated `out/` artifacts; ex1 and ex4 need no LLM |
| Last raw model reply | `out/last_llm_reply.txt` |
