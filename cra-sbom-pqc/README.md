# EU Cyber Resilience Act, SBOM and post-quantum migration

What the CRA requires from manufacturers (24 h / 72 h / 14-day vulnerability reporting applying since 11 Sep 2026, full application 11 Dec 2027), what an SBOM must and
should contain (CRA Annex I, BSI TR-03183-2, CISA 2026 minimum elements), how to scan and use VEX, and how to build a crypto inventory (CBOM) and a post-quantum plan
(NIST FIPS 203/204/205, NIST IR 8547 dates, EU PQC roadmap, hybrid ML-KEM in TLS), with a runnable workshop that measures each step.

> **General information, not legal advice.** Engineering-oriented reading of public sources as of 2026-11-16.

- [`research.md`](research.md) - sources (checked 2026-11-16) with ✅/🟡/🟠/❌/🧪/🔮 markers: CRA text (read on EUR-Lex), reporting clock, SBOM requirements, PQC status, our measurements, consensus vs disputed, open items
- [`comparison.md`](comparison.md) - SBOM generators, formats, scanners and VEX, reporting operations, crypto inventory sources, PQC migration options; decision guide
- [`talk-outline.md`](talk-outline.md) - ~35 min talk, 9 segments with timing
- [`talk-script.md`](talk-script.md) + [`presentation/`](presentation/) - read-aloud script and 25-slide serious Excalidraw deck (PDF, per-slide PNG/SVG, speaker notes, QR)
- [`workshop-plan.md`](workshop-plan.md) + [`workshop/`](workshop/) - 5 labs (SBOM gaps, scan + KEV + VEX, the 24 h clock, crypto inventory/CBOM, hybrid ML-KEM TLS) with real measured results; free OpenRouter models only (one optional step), everything else offline or against public databases

Quick start:

```bash
cd workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./setup_tools.sh                       # syft, grype, osv-scanner into ./.tools/bin
python -m pytest -q tests
python ex1_sbom/run_sbom.py && python ex2_vuln_vex/scan.py && python ex2_vuln_vex/vex.py
python ex4_crypto_inventory/scan_crypto.py
python ex5_pqc_tls/pqc_tls_lab.py      # needs OpenSSL >= 3.5
```

Status: Stage 2 done (2026-11-16): talk script (~35 min + Q&A) and a 25-slide Excalidraw deck with read-aloud notes in [`presentation/`](presentation/). Participant guide and root README row: not yet.
