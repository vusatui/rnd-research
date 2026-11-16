# Talk outline (~35 min): "Twenty-four hours to report, ten years to migrate: CRA reporting, SBOMs and the post-quantum plan"

> General information, not legal advice. Audience: engineers, architects, security and delivery leads who ship software or devices to the EU.
> Goal: understand what the CRA already requires today (reporting since 11 Sep 2026), what an SBOM must and must not be, and how to turn "PQC plan" into an inventory plus one measured pilot - with numbers from our workshop.
> Legend: ✅ verified source, 🟡 vendor claim, 🟠 secondary, ❌ unverified, 🧪 measured in our workshop, 🔮 forecast (see `research.md`, `workshop-plan.md`).

| # | Min | Section | Content | Visual / demo |
|---|---|---|---|---|
| 1 | 0-3 | Hook | A scanner shows "KEV: yes" on a library in your product at 09:00 Monday. Who decides it is reportable, who submits, what is due at 09:00 Tuesday? 156 findings on a small sample, one of them known-exploited 🧪 | scan table with the single red row |
| 2 | 3-8 | What the CRA requires and when | Art. 14 since 11 Sep 2026 incl. products already on the market (Art. 69(3)); full application 11 Dec 2027; fines EUR 15 M / 2.5 % ✅ | timeline: Jun 2026, Sep 2026, Dec 2027 |
| 3 | 8-13 | The reporting clock | actively exploited vs severe incident; 24 h / 72 h / 14 d after a *mitigating* measure / 1 month after the 72 h notice; one submission via the ENISA SRP to the home CSIRT + ENISA ✅. Live: `cra_clock.py` and `draft.py` 🧪 | clock diagram, terminal |
| 4 | 13-18 | SBOM: what it is and is not | Annex I Part II(1): top-level deps minimum ✅; BSI TR-03183-2 and CISA 2026 elements raise the bar ✅; our syft SBOM scored 46.6 % / 47.9 % raw, 67.0 % / 70.8 % enriched 🧪; why transitive gaps matter (osv-scanner found 3 more packages) 🧪 | coverage bars before/after |
| 5 | 18-21 | From SBOM to decisions: scan, VEX, KEV | grype vs osv-scanner; VEX 156 -> 137 with a human in the loop; the LLM-drafted advisory that inflated severity 4 of 4 times 🧪 | funnel 156 -> 137 -> 1 |
| 6 | 21-25 | The PQC clock | NIST IR 8547: deprecate after 2030, disallow after 2035 ✅; EU roadmap: start 2026, high-risk 2030, rest 2035 (addressed to Member States) ✅; harvest-now-decrypt-later; CRQC date is a forecast 🔮 | three-line timeline, "who is it addressed to" tag |
| 7 | 25-29 | Crypto inventory and ranking | CBOM concept; our scan of the sample: 32 findings; Mosca X+Y>Z with three Z values; the ranking changes with Z, so say your Z out loud 🧪 | ranking table, Z slider |
| 8 | 29-32 | Hybrid ML-KEM in practice | X25519MLKEM768 negotiated by default with OpenSSL 3.5 🧪; +1.2 kB / +1.1 kB; fallback and failure cases; ML-DSA sizes 🧪; what we did not test (browsers, CAs, HSMs) | bytes bar chart |
| 9 | 32-35 | Plan and Q&A seeds | 90-day plan: reporting drill, build-time SBOM, two scanners, inventory, one hybrid pilot; limits and open items; link to the repo | checklist slide + QR |
| - | 35-40 | Q&A | see `talk-script.md` Q&A section | |

Fallback if the demo fails: all outputs are committed in `workshop/results/`.
