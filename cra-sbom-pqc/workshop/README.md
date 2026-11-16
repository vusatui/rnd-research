# Workshop: CRA reporting, SBOM and the post-quantum plan

Five hands-on labs on a fictional, deliberately outdated product ("acme-gateway"). **General information, not legal advice**; nothing here is a conformity
assessment. The sample has known vulnerabilities on purpose - never deploy it. Deadlines come from Regulation (EU) 2024/2847 Art. 14; see `../research.md`.

| Lab | What you do | Needs |
|---|---|---|
| `ex1_sbom/` | Generate a CycloneDX SBOM with **syft**, check it against CRA Annex I Part II(1), BSI TR-03183-2 v2.1.0 and the CISA 2026 minimum elements, enrich it honestly, re-check | syft |
| `ex2_vuln_vex/` | Scan with **grype** and **osv-scanner**, compare, flag known-exploited (CISA KEV) findings, write **OpenVEX** for unused direct dependencies and measure the effect | grype, osv-scanner, network |
| `ex3_reporting/` | **CRA Art. 14 clock** (24 h / 72 h / 14 d / 1 month), draft the three submissions from the KEV finding, optional free-model advisory + fact guard | optional free OpenRouter key |
| `ex4_crypto_inventory/` | Regex **crypto inventory** of the sample -> CycloneDX 1.6 **CBOM**, ranking by Mosca's inequality at several Z | nothing |
| `ex5_pqc_tls/` | **Hybrid ML-KEM (X25519MLKEM768)** in TLS 1.3 with OpenSSL 3.5, byte counts, interop failures, ML-DSA certificate sizes, endpoint probing | OpenSSL >= 3.5 |

## Quick start

```bash
cd workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./setup_tools.sh                                # syft 1.57.1, grype 0.121.3, osv-scanner 2.7.1 into ./.tools/bin (no root)
python -m pytest -q tests                       # offline unit tests; tool/openssl-dependent ones skip themselves
python ex1_sbom/run_sbom.py                     # writes out/sbom*.json, results/ex1_sbom_<date>.json
python ex2_vuln_vex/scan.py                     # needs ex1 first; results/ex2_scan_<date>.json
python ex2_vuln_vex/vex.py
python ex3_reporting/cra_clock.py vulnerability --aware 2026-11-16T09:00:00Z --now 2026-11-17T10:00:00Z --corrective 2026-11-18T15:00:00Z
python ex3_reporting/draft.py                   # deterministic drafts; add --llm for ONE free-model request
python ex4_crypto_inventory/scan_crypto.py --z 8,12,15
python ex5_pqc_tls/pqc_tls_lab.py --n 30
```

Optional LLM step (ex3 `--llm`): `cp .env.example .env`, put a free key from https://openrouter.ai/keys into `OPENROUTER_API_KEY` (or export it);
**free models only** (`:free`). `python check_quota.py` shows the daily free requests left; `python list_free_models.py` lists current free models.
The client (`common/llm.py`) throttles, disables reasoning and never prints the key.

## Results committed in `results/` (2026-11-16)

| File | What |
|---|---|
| `ex1_sbom_2026-11-16.json`, `ex1_sbom_output.txt` | field coverage before/after enrichment (BSI, CISA 2026) |
| `ex2_scan_2026-11-16.json`, `ex2_scan_output.txt` | grype vs osv-scanner, KEV hits (grype DB built 2026-11-15) |
| `ex2_vex_2026-11-16.json`, `ex2_vex_output.txt` | VEX effect: 156 -> 137 findings |
| `ex3_clock_example.txt`, `ex3_draft_llm_output.json` | clock output, drafts and one free-model advisory with the guard result |
| `ex4_inventory_2026-11-16.json`, `ex4_inventory_output.txt` | crypto findings and the ranking |
| `ex5_pqc_tls_2026-11-16.json`, `ex5_pqc_tls_output.txt` | handshake bytes, interop, sizes, probe |

Vulnerability counts depend on the database build date; re-running tomorrow gives different numbers. Timings include process start.

## What to look at

1. `ex1_sbom/check_sbom.py` - which fields each yardstick wants; `enrich.py` adds only derivable facts (lockfile SHA-512, `resolved` URL, author you declare, lifecycle, `compositions`).
2. `ex2_vuln_vex/scan.py` - why two scanners; `vex.py` - the import check and the OpenVEX statement (it is a *candidate*, not a decision).
3. `ex3_reporting/cra_clock.py` - the arithmetic and its edge cases (`tests/test_labs.py`); `draft.py` - the legal minimum for each submission, not the SRP form.
4. `ex4_crypto_inventory/rules.py` + `assets.json` - the rules and the fictional business context; run with `--z 5,10,20`.
5. `ex5_pqc_tls/pqc_tls_lab.py` - part B shows the two ways migrations fail in practice.
