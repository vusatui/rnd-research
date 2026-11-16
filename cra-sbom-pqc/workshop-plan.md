# Workshop plan: "Report in 24 hours, inventory your crypto, try a hybrid handshake" (~2 h)

> General information, not legal advice. The labs demonstrate **mechanisms and measurements** on a fictional, deliberately outdated product ("acme-gateway");
> they are not a conformity test and say nothing about any vendor product. Code: [`workshop/`](workshop/); setup, budgets, troubleshooting: [`workshop/README.md`](workshop/README.md);
> step-by-step guide: [`workshop/PARTICIPANTS.md`](workshop/PARTICIPANTS.md).

Participants play the manufacturer of a small gateway product (Python service + Node console + Java legacy + nginx/sshd config).

| # | Time | Exercise | Needs | What participants do / learn |
|---|---|---|---|---|
| 0 | 10 min | Setup | Python >= 3.10, curl, OpenSSL >= 3.5 (only for ex5) | venv, `pip install -r requirements.txt`, `./setup_tools.sh` (syft, grype, osv-scanner into `.tools/`), `pytest -q tests` |
| 1 | 25 min | **SBOM and its gaps** (`ex1_sbom/`) | syft | Generate CycloneDX with syft, run the BSI / CISA field check, enrich only with facts you know, compare coverage, see what a tool cannot invent |
| 2 | 25 min | **Scan, KEV, VEX** (`ex2_vuln_vex/`) | grype, osv-scanner, network | Scan the SBOM and the lockfiles with two engines, read the overlap, find the KEV hit, generate OpenVEX candidates and measure the effect; decide which statements you would sign |
| 3 | 25 min | **The 24 h clock** (`ex3_reporting/`) | optional free OpenRouter key (1-2 requests) | Compute deadlines (`cra_clock.py`), draft early warning / notification / final report from the KEV finding, optionally ask a free model for a customer advisory and read what the fact guard flags |
| 4 | 25 min | **Crypto inventory and ranking** (`ex4_crypto_inventory/`) | none | Scan the sample for quantum-vulnerable crypto, validate the CBOM, change Z and watch the backlog reorder; add a rule for something the scanner misses |
| 5 | 25 min | **Hybrid ML-KEM and PQ certificates** (`ex5_pqc_tls/`) | OpenSSL >= 3.5 | Measure bytes for classical / hybrid / pure groups across six certificate types, break interop on purpose (hybrid-only client, default server vs pure ML-KEM), read the sizes table |
| - | 5 min | Wrap-up | | Fill the 90-day plan from `talk-outline.md` |

Stretch goals: run cdxgen and compare to syft; add a CycloneDX-VEX output; point `scan_crypto.py` at your own repo; add `ssl_ecdh_curve`-style rules for your stack; probe a public TLS endpoint you own with `pqc_tls_lab.probe`-style code;
add an SPDX 3.0.1 output and check it against BSI's mapping; model the NIS2/CRA double reporting in the clock.

## Commands (also in `workshop/README.md`)

```bash
cd cra-sbom-pqc/workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./setup_tools.sh                          # ~1 min; installs into ./.tools/bin
export PATH="$PWD/.tools/bin:$PATH"       # optional: the labs also look there themselves
python -m pytest -q tests                 # offline unit tests (19)
python ex1_sbom/run_sbom.py               # ~2 s
python ex2_vuln_vex/scan.py               # ~10 s (first run downloads the grype DB; osv-scanner needs network)
python ex2_vuln_vex/vex.py
python ex3_reporting/cra_clock.py vulnerability --aware 2026-11-16T09:00:00Z --now 2026-11-17T10:00:00Z --corrective 2026-11-18T15:00:00Z
python ex3_reporting/draft.py [--llm]     # --llm: 1 free-model request, needs OPENROUTER_API_KEY
python ex4_crypto_inventory/scan_crypto.py --z 8,12,15
python ex5_pqc_tls/pqc_tls_lab.py --n 30  # ~15 s, needs OpenSSL >= 3.5
```

## Measured results (2026-11-16, our box: Linux, Python 3.13, OpenSSL 3.5.7, syft 1.57.1, grype 0.121.3 (DB 2026-11-15), osv-scanner 2.7.1)

Raw outputs: [`workshop/results/`](workshop/results/). The vulnerability counts depend on the database build date and will differ when you re-run.

| Lab | Measurement |
|---|---|
| ex1 | 72 components, 0.97 s. BSI per-component field coverage 46.6 % -> 67.0 % after enrichment; CISA per-component 47.9 % -> 70.8 %; SBOM-level BSI 75 % -> 100 %, CISA 50 % -> 87.5 %. Still 0 %: component creator/supplier, source URI. |
| ex2 | grype 156 findings / 15 packages (1 KEV). osv-scanner 18 packages / 215 vulns. Overlap 15 packages; osv-only: certifi, idna, urllib3 (transitive). VEX candidates: pyyaml, requests, jinja2, lodash, minimist, express -> 19 statements -> 137 findings. |
| ex3 | clock example: aware 2026-11-16 09:00Z -> early warning due 2026-11-17 09:00Z, notification 2026-11-19 09:00Z, final report 14 days after the mitigating measure (2026-12-02 15:00Z). Free model advisory: severity inflation flagged in 4 of 4 runs. |
| ex4 | 32 findings / 5 files / 13 CBOM components; ranking at Z = 8 / 12 / 15: 5 / 4 / 0 assets "migrate now". |
| ex5 | see `workshop/results/ex5_pqc_tls_output.txt`: ClientHello 330 B (X25519) vs 1506 B (X25519MLKEM768); ECDSA server flight 806 -> 1895 B; ML-DSA-65 server flight 9.2 -> 10.2 kB; classical-only server + hybrid-only client = 0/5; default server + pure ML-KEM client = 0/5. |

Honest limits: see `research.md` section 6.
