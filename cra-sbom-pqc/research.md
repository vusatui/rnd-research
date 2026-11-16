# Cyber Resilience Act, SBOM and post-quantum migration - research notes

> **General information, not legal advice.** Engineering-oriented reading of public sources as of **2026-11-16**. Whether a product is in scope
> of the CRA, who is the "manufacturer", whether something is an "actively exploited vulnerability" or a "severe incident", and what is
> sufficient are legal questions for counsel and the competent authorities. Nothing here is a conformity assessment.

Question behind the topic (typical client ask): *"24 h vulnerability reporting; crypto inventory and PQC plan - what exactly must we do, what do the
official documents say, and what can we build and measure today?"*

Legend (same as the other topics):
- ✅ **verified**: read on the primary page (regulation text, authority page/PDF, standard, our own tool output).
- 🟡 **vendor-claim**: a vendor/product describing itself.
- 🟠 **secondary**: law-firm/blog/press/tracker, or a primary page known to us only through a search-result summary.
- ❌ **unpublished / unverified / disputed**.
- 🧪 **measured by us** in the workshop (`workshop/`, raw results in `workshop/results/`).
- 🔮 **forecast / expectation**, not a fact.

## TL;DR (key findings)

1. **The CRA reporting duty is live.** Regulation (EU) 2024/2847 applies in full from **11 December 2027**, but **Art. 14 (reporting) applies from
   11 September 2026** and Chapter IV (notified bodies) from 11 June 2026 ✅ ([Art. 71(2), EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng);
   [EC reporting page](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting)). It was in force since 10 December 2024 (EC guidance page says "in force since December 2024") ✅.
   It is the one obligation that already binds, **including for products placed on the market before 11 Dec 2027**: Art. 69(2) exempts old products from the rest of the Regulation unless substantially modified, but
   Art. 69(3) says *"the obligations laid down in Article 14 shall apply to all products with digital elements that fall within the scope of this Regulation that have been placed on the market before 11 December 2027"* ✅.
   Whether a given product is "in scope" and who is its "manufacturer" remain legal questions ❌.
2. **The clock is 24 h / 72 h / 14 days (vulnerabilities) and 24 h / 72 h / 1 month (severe incidents)** ✅ Art. 14(2) and 14(4):
   early warning "without undue delay and in any event within 24 hours of the manufacturer becoming aware"; vulnerability or incident notification within 72 h; final report
   **no later than 14 days after a corrective or mitigating measure is available** (vulnerabilities) or **within one month after the 72 h incident notification** (incidents). One submission, via ENISA's
   **Single Reporting Platform (SRP)**, simultaneously to the CSIRT of the manufacturer's main establishment and to ENISA (Art. 14(1), 14(7), Art. 16) ✅. The SRP has been operational since 11 Sep 2026 and was upgraded to v1.3 on 4 Nov 2026 ✅ ([ENISA SRP page](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp)).
3. **Reporting is only triggered by "actively exploited" vulnerabilities and "severe" incidents**, not by every CVE ✅ Art. 3(42): *"reliable evidence that a malicious actor has exploited it in a system without permission of the system owner"*;
   Art. 14(5): an incident is severe if it negatively affects (or can affect) availability, authenticity, integrity or confidentiality of sensitive or important data/functions, or has led (or can lead) to malicious code in the product or user networks.
   Users must be informed too, "where appropriate in a structured, machine-readable format" (Art. 14(8)) ✅. Fines for breaching Arts. 13 and 14: up to **EUR 15 000 000 or 2.5 % of worldwide annual turnover**, whichever is higher (Art. 64(2)) ✅.
4. **An SBOM is a legal requirement but a thin one.** Annex I Part II(1): *"drawing up a software bill of materials in a commonly used and machine-readable format covering at the very least the top-level dependencies"*; it is
   technical documentation (Annex VII) given to market-surveillance authorities on reasoned request (Annex VII point 8), and the manufacturer *may* (not must) give it to users (Annex II point 9) ✅.
   The CRA does **not** name a format or field list; the Commission *may* specify format and elements by implementing act (Art. 13(24)) ✅ - we found none ❌ (unverified; check the OJ).
   Practical bars are set by other documents: BSI TR-03183-2 v2.1.0 (CycloneDX >= 1.6 / SPDX >= 3.0.1, SHA-512, creator e-mail/URL ...; **not** a presumption of conformity) ✅, and the
   CISA-led **2026 Minimum Elements** (29 Jul 2026; voluntary, US-led, 18 agencies on the cover incl. BSI and ANSSI) ✅.
5. **No harmonised standard gives a presumption of conformity yet** (🟠 tracker; EC says standardisation request M/606 with 41 standards was amended on 10 Nov 2026 to extend some deadlines by 3 months ✅
   [EC standardisation page](https://digital-strategy.ec.europa.eu/en/policies/cra-standardisation)). The Commission's non-binding guidance (27 Jul 2026, 67 examples) is the main official interpretation ✅ (we read the announcement page, not the 100+ page guidance itself ❌).
6. **The CRA does not mandate post-quantum cryptography.** It requires protection of confidentiality "by state of the art mechanisms" (Annex I Part I(2)(e)) ✅ - "state of the art" will move toward PQC, but that is our inference 🔮.
   PQC is driven by **NIST/EU roadmaps**: FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA) final since 13 Aug 2024 ✅; **NIST IR 8547 final (Oct 2026)**: quantum-vulnerable public-key crypto (RSA, ECDSA, EdDSA, DH/ECDH) **deprecated after 2030, disallowed after 2035** in NIST standards; ML-KEM-768 recommended default ✅ (we read the PDF);
   the **EU Coordinated Implementation Roadmap (June 2025)** asks Member States to start by **end of 2026**, finish **high-risk use cases by end of 2030** and as much as feasible by **2035** ✅ - it is addressed to Member States, not a company obligation ✅.
7. **Harvest-now-decrypt-later is the argument that makes PQC urgent for key exchange; signatures are a different, slower problem.** The Commission page says data that must remain confidential for a long time "may be already at risk" and
   "store now, decrypt later" attacks "are already likely occurring" ✅ (EC statement, not measured). That is why **hybrid key exchange (X25519MLKEM768)** is the first thing deployed: RFC 10024 (Aug 2026, Standards Track) ✅, enabled by default in OpenSSL 3.5 ✅ and measured by us 🧪.
8. **What we measured** 🧪 (Nov 16 2026, one box, synthetic target): syft SBOM of a 72-component sample fails the BSI creator, SHA-512 and URI fields out of the box; an honest enrichment lifts BSI per-component coverage from 46.6 % to 67.0 % but cannot invent supplier or licence data;
   grype vs osv-scanner find the same 15 vulnerable packages but osv-scanner finds 3 more (transitive Python packages syft's requirements.txt cataloguer never listed); VEX for 6 unused direct dependencies removes 19 of 156 findings; a KEV hit (Pillow/libwebp) starts the reporting clock;
   a regex "CBOM" finds 32 crypto usages in 5 files and ranks them by Mosca's inequality; hybrid ML-KEM costs ~1.2 kB client and ~1.1 kB server bytes per handshake with no visible time difference at ~10 ms resolution, while an ML-DSA-65 certificate chain adds ~8 kB.

## 1. CRA: what the text says

All quotes are from the consolidated OJ text of Regulation (EU) 2024/2847 read on EUR-Lex on 2026-11-16 ✅ ([ELI link](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng)).

### 1.1 Dates

| Date | What | Source |
|---|---|---|
| 10 Dec 2024 (20th day after OJ publication of 20 Nov 2024) | entry into force | Art. 71(1) ✅ (date arithmetic ours) |
| 11 Jun 2026 | Chapter IV (Arts. 35-51, notification of conformity assessment bodies) applies | Art. 71(2) ✅ |
| **11 Sep 2026** | **Art. 14 reporting obligations apply**; ENISA SRP operational | Art. 71(2) ✅, [EC](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting) ✅, [ENISA](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp) ✅ |
| **11 Dec 2027** | Regulation applies in full (essential requirements, conformity assessment, CE marking, SBOM duty); open-source steward reporting (Art. 24(3)) | Art. 71(2) ✅, EC page ✅ |

### 1.2 Reporting (Art. 14) and who reports to whom

| Step | Vulnerability actively exploited (14(2)) | Severe incident (14(4)) |
|---|---|---|
| Early warning | without undue delay, **<= 24 h** after becoming aware; indicate Member States where the product is available | <= 24 h; at least whether suspected unlawful/malicious; Member States |
| Notification | **<= 72 h** (unless already provided): general product info, general nature of exploit and vulnerability, corrective/mitigating measures taken and for users, **sensitivity** of the information | <= 72 h: nature, initial assessment, measures, sensitivity |
| Final report | **<= 14 days after a corrective *or mitigating* measure is available**: description incl. severity/impact, malicious actor (if available), details of update/measure | **within one month after the 72 h notification**: detailed description, threat type/root cause, mitigation applied/ongoing |

- Channel: SRP, via the end-point of the CSIRT designated as coordinator in the Member State of the **main establishment** (where cybersecurity decisions are predominantly taken; fallback rules for non-EU manufacturers use the authorised representative's Member State, Art. 14(7)); simultaneously accessible to ENISA ✅.
- CSIRTs may delay dissemination to other CSIRTs on justified cybersecurity grounds (Art. 16(2)); the Commission delegated act specifying those grounds was adopted 11 Dec 2025 per the EC page 🟠 (we read the EC page's statement and link `CELEX:32026R0881`, not the act).
- The CSIRT may request intermediate reports (14(6)); notifying does not "subject the notifying person to increased liability" (Art. 17(4)) ✅.
- Art. 14(10): the Commission *may* specify format and procedure by implementing act ✅. We did not find one ❌; the SRP glossary/guidance is where the actual fields live (not read in detail ❌).
- Users: inform impacted users (and where appropriate all users) of the vulnerability/incident and mitigations, machine-readable where appropriate (14(8)) ✅.
- Upstream: when you find a vulnerability in a component (incl. open source), report it to the maintainer and share your fix where appropriate (Art. 13(6)) ✅.

"Becomes aware" is not defined in the article text beyond the phrase itself ❌ - document when and how awareness arose. "Corrective or mitigating measure" in the 14-day rule means the clock can start before a full patch exists ✅ (text), which our `cra_clock.py` models.

### 1.3 Vulnerability handling and the SBOM (Annex I Part II, Art. 13)

- Annex I Part II(1): identify and document vulnerabilities and components, incl. an SBOM in a commonly used, machine-readable format covering **at least the top-level dependencies** ✅.
- II(2)-(8): fix without delay (separately from feature updates where feasible), regular testing, **public disclosure of fixed vulnerabilities** once an update exists, a **coordinated vulnerability disclosure policy**, a contact address for reports, secure update distribution, free security updates with advisories ✅.
- Art. 13(8): **support period at least five years** (or expected use time if shorter), documented in technical documentation; Art. 13(9): each security update remains available **at least 10 years or the rest of the support period**, whichever is longer ✅; Art. 13(13): technical documentation and EU declaration kept 10 years (or support period) ✅.
- Art. 13(5): due diligence when integrating third-party and open-source components ✅.
- Annex I Part I(2)(a): products placed on the market **without known exploitable vulnerabilities**; (e): encrypt data at rest/in transit "by state of the art mechanisms" ✅.
- Annex VII(8): the SBOM is handed to the market-surveillance authority "further to a reasoned request" ✅; Annex II(9): if the manufacturer decides to make it available to users, say where ✅.
- Art. 13(24) allows the Commission to specify SBOM format and elements by implementing act ✅ - none found ❌.

### 1.4 Other points worth knowing

- Fines: Art. 64(2): breaches of Annex I requirements and Arts. 13, 14: up to EUR 15 M / 2.5 % turnover; Art. 64(3): other listed obligations EUR 10 M / 2 % ✅.
- Open-source stewards: lighter regime (Art. 24; reporting from 11 Dec 2027) ✅. "Important" and "critical" product classes (Annexes III, IV) need stricter conformity assessment ✅ (not detailed here).
- Standards: M/606, 41 standards, deadlines extended on 10 Nov 2026 ✅ (EC page). Harmonised standards cited in OJ: none found 🟠 ([tracker](https://craevidence.com/cra-compliance/harmonised-standards-status) - secondary; verify in the OJ).
- Commission guidance (27 Jul 2026, non-binding, scope incl. remote data processing and FOSS, substantial modification, support periods, reporting, risk assessment) ✅ announcement read; full guidance and FAQ not read ❌.
- The Digital Omnibus (Nov 2025) is mentioned by the Commission as part of simplification; whether it changes CRA reporting is **not researched** ❌ (open item).

## 2. SBOM: formats, minimum elements, tools

| Source | What it demands | Status |
|---|---|---|
| CRA Annex I Part II(1) | machine-readable, commonly used format, >= top-level dependencies | law ✅ |
| [BSI TR-03183-2 v2.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile) (Aug 2025) | CycloneDX **>= 1.6** or SPDX **>= 3.0.1** JSON/XML; SBOM creator e-mail/URL, timestamp; per component: creator, name, version, filename, dependencies (+ completeness), licences, **SHA-512** of the deployable, executable/archive/structured properties; "An SBOM MUST NOT contain vulnerability information" | German technical guideline, "not binding", "cannot be used as presumption of conformity" ✅ ([BSI page](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03183/TR-03183_node.html)) |
| [CISA et al. 2026 Minimum Elements](https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom) (29 Jul 2026) | replaces NTIA 2021; new: SBOM Author Signature, Data Format Name/Version, Generation Context, Tool Name/Version, SBOM Version, Component Hash Value/Algorithm, Component License; major updates: SBOM Author, Component Identifiers, Producer, Version, Coverage, Explicitly Identifying Unknown Information, Machine-Processable Data | voluntary guidance, 18 agencies on the cover incl. BSI and ANSSI ✅ (PDF read) |
| CycloneDX / SPDX | formats. CycloneDX 1.7 is [ECMA-424 2nd edition (Dec 2025)](https://ecma-international.org/publications-and-standards/standards/ecma-424/) ✅; ISO/IEC DIS 27055 listed as the ISO number ✅ | standards |

Note the tension we measured 🧪: BSI says an SBOM **must not** carry vulnerability data (it is static; vulnerabilities change), which is why **VEX** is a separate document. CISA's 2026 list adds hashes, licences and tool provenance. A syft default SBOM is a good start and fails several of these fields (section 6).

Tooling facts (our measurements, versions pinned in `workshop/setup_tools.sh`): syft 1.57.1 (CycloneDX 1.7 default JSON output), grype 0.121.3 (DB built 2026-11-15), osv-scanner 2.7.1 🧪.

## 3. Post-quantum cryptography: status

| Item | Status | Source |
|---|---|---|
| FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA | final, published 13 Aug 2024 | [NIST CSRC PQC project page](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post_Quantum_Cryptography-Standardization) ✅ (via search result text) |
| FIPS 206 FN-DSA (Falcon) | **not published**; NIST IR 8547 says a FIPS is "under development" | IR 8547 ✅; secondary trackers say no public draft as of Nov 2026 🟠 |
| HQC | selected 11 Mar 2025 as an alternative KEM; FIPS "under development" | CSRC ✅; IR 8547 ✅ |
| [NIST IR 8547 final](https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8547.pdf) (Oct 2026; initial draft Nov 2024 withdrawn - 🟠) | "NIST will deprecate quantum-vulnerable public-key cryptography after 2030 and disallow its use under NIST standards and guidelines after 2035"; ML-KEM-768 "recommended as the default parameter set"; federal high-value/high-impact systems: PQC key establishment by 31 Dec 2030, signatures by 31 Dec 2031 (EO 14412 / OMB M-26-15); hybrids "typically expected to be temporary measures" | PDF read ✅ (US federal context) |
| [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024.html) | Standards Track (Aug 2026): X25519MLKEM768, SecP256r1MLKEM768, SecP384r1MLKEM1024 for TLS 1.3; client share for X25519MLKEM768 is 1216 bytes | ✅ read |
| OpenSSL 3.5 (LTS to 8 Apr 2030) | ML-KEM, ML-DSA, SLH-DSA; default TLS groups prefer X25519MLKEM768; client sends X25519MLKEM768 and X25519 key shares | [release notes](https://openssl.org/news/openssl-3.5-notes/) ✅ (via search result text) + 🧪 |
| [EU Coordinated Implementation Roadmap](https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography) (NIS Cooperation Group, 23 Jun 2025) | Member States: first steps (incl. "support mature cryptographic asset management", dependency maps, quantum risk analysis, include the supply chain) by **31 Dec 2026**; **high-risk use cases by 31 Dec 2030**; **medium-risk by 31 Dec 2035**; low-risk "as much as feasible"; "use standardised and tested hybrid solutions, whenever feasible and suitable"; quantum-vulnerable public-key mechanisms "shall not be used stand-alone" after 2030 (high-risk) / 2035 (medium-risk) | PDF read ✅ - addressed to Member States ✅ |
| [EC PQC page](https://digital-strategy.ec.europa.eu/en/policies/post-quantum-cryptography) (updated 20 Oct 2026) | Recommendation of April 2024; roadmap June 2025; FAQ and survey feedback published; a second deliverable "in preparation" | ✅ read |
| CBOM | CycloneDX 1.6+ models cryptographic assets as components of type `cryptographic-asset` with `cryptoProperties` | [CycloneDX guide](https://cyclonedx.org/guides/OWASP%5FCycloneDX-Authoritative-Guide-to-CBOM-en.pdf) 🟠; schema validated by us 🧪 |

Not found / not claimed: the date a cryptographically relevant quantum computer (CRQC) will exist. That is a **forecast** 🔮 and the single biggest parameter in any migration business case; we expose it as a parameter (`Z`) instead of picking a number.
BSI/ANSSI/NCSC national positions (e.g. on hybrids vs pure PQC) are linked from the EC page but were not read ❌.

### 3.1 Why signatures and key exchange are different problems (engineering reading)
- **Key exchange / encryption**: recorded traffic can be decrypted later (harvest now, decrypt later) - the EC page says so ✅. Fix = hybrid KEM now; cost ~1 kB per direction 🧪.
- **Signatures / certificates**: an attacker needs a quantum computer *at forgery time*, so the risk is about long-lived roots, firmware signing keys and devices you cannot update. Sizes explode (ML-DSA-65 certificate 5.5 kB vs ECDSA 0.4 kB 🧪), and the WebPKI/ecosystem for PQ certificates is not something we tested ❌.
- The Mosca inequality (X + Y > Z, secrecy lifetime + migration time vs time-to-CRQC) is a *planning heuristic* 🟠 (we cite it as common practice; no primary source checked ❌).

## 4. What our workshop measured 🧪 (details: [`workshop/README.md`](workshop/README.md), raw: [`workshop/results/`](workshop/results/))

All on one Linux box, 2026-11-16, synthetic fictional target "acme-gateway" (deliberately old pins: Python 5 direct deps, Node 4 direct / 66 locked packages).

| Lab | Result |
|---|---|
| ex1 SBOM | syft 1.57.1 -> CycloneDX 1.7, **72 components in ~1 s** (Python: only the 5 direct pins; Node: full lock tree). Coverage of machine-checkable fields: BSI per-component **46.6 %**, CISA per-component **47.9 %** raw; after our honest enrichment (npm integrity SHA-512 + `resolved` URL, SBOM author, lifecycle phase, `compositions`) **67.0 % / 70.8 %**. Still 0 % for component creator/supplier and source URIs: no tool can invent those. Output validates against the CycloneDX schema (Python lib). |
| ex2 scan | grype: **156 findings (16 critical, 79 high, 50 medium, 11 low) in 15 packages**; osv-scanner: **18 packages / 215 vulnerabilities** (aliases counted differently: 228 vs 416 distinct IDs). osv-scanner resolved 3 transitive Python packages (certifi, idna, urllib3) the SBOM did not contain - **an SBOM-coverage gap, not a scanner bug**. 1 finding is in CISA KEV (Pillow 8.1.0, CVE-2023-4863 libwebp) - the plausible Art. 14 trigger. **VEX**: 6 direct dependencies not imported by first-party code -> 19 statements -> **156 -> 137 findings**; the KEV finding stays (Pillow is imported). |
| ex3 reporting | `cra_clock.py` computes 24 h / 72 h / 14 d / 1 month from awareness; tested on edge cases (month clamp, late/on-time, clock not started). `draft.py` writes the three Art. 14(2) submissions from the KEV finding. One optional free-model call drafts a customer advisory: **in 4 of 4 runs (the last 3 with the guard) the model added claims not in the facts** (e.g. "critical", "remote code execution", "immediately"); a keyword guard flags them. |
| ex4 inventory | regex rules over 5 files -> **32 findings, 13 CBOM components** (CycloneDX 1.6, schema-valid); 8 RSA, 5 ECDH, 2 ECDSA, 5 P-curve keys, 1 Ed25519, 3 X25519 vs MD5 (1), SHA-1 (1), AES-256-GCM (1). Ranking by Mosca for Z = 8 / 12 / 15 years: **4 assets "migrate now" at Z=12, 5 at Z=8, 0 at Z=15**. |
| ex5 PQC TLS | OpenSSL 3.5.7: default client negotiates **X25519MLKEM768** against a default server 6/6 certificate types. ClientHello **330 -> 1506 B**, server flight **+~1.1 kB** (e.g. ECDSA 806 -> 1895 B). Time per handshake indistinguishable (~10.5 ms, process-start dominated). A **classical-only server** still works with a default client (fallback to X25519) but **fails 0/5 if the client offers only the hybrid group**; a **default OpenSSL 3.5 server rejects clients offering only pure MLKEM768 or SecP256r1MLKEM768 (0/5)** - those groups must be enabled explicitly. ML-DSA-44/65/87 certificates work in TLS 1.3 with OpenSSL 3.5.7 (server flight 6.8 / 9.2 / 12.4 kB vs 0.8 kB for ECDSA). |

## 5. Consensus vs. disputed vs. open

**Reasonably settled (primary sources agree):** CRA dates and the 24 h / 72 h / 14 d clock; SRP as the single channel; SBOM needs top-level dependencies at minimum; NIST 2030/2035 dates for deprecation and disallowance; ML-KEM-768 as the recommended parameter set; hybrids are the transition tool in EU and NIST texts.

**Disputed / unsettled:**
- What counts as "reliable evidence" of active exploitation, and when a manufacturer "becomes aware" - legal judgement ❌. KEV listing is a strong public signal, not the legal test.
- Whether the SBOM should be handed to customers (CRA: optional), and its depth (CRA: top-level; BSI/CISA: full coverage incl. transitive).
- Hybrid vs. pure PQC: EU roadmap recommends hybrid "whenever feasible and suitable"; NIST IR 8547 says hybrids add complexity and are expected to be temporary ✅; other national agencies' positions not read ❌.
- CRQC arrival 🔮: unknown; forecasts differ. Treat as a scenario parameter.
- Pure-PQC certificates in the public WebPKI: not tested, not researched ❌.

**Open items ❌:** SRP field list and any Art. 14(10) implementing act; Commission CRA guidance sections 9.1 (reporting) in full; the delegated act on withholding; harmonised standards status in the OJ; Digital Omnibus effect on CRA/NIS2 reporting; NIS2/DORA overlaps with CRA reporting (single entry point plans); FIPS 206 / HQC FIPS dates (unpublished); real-world PQ certificate support in browsers/CAs.

## 6. Limits of our workshop
- Synthetic, deliberately outdated app; counts change daily with vulnerability databases (we pin tool versions and record the DB build date, 2026-11-15).
- The crypto scanner is a regex "grep with opinions": it does not see binaries, third-party library internals, HSMs or data encrypted elsewhere. Production inventory needs several sources (code, dependencies, network probes, certificate stores, KMS).
- The VEX "reachability" is an import check; real VEX needs engineers who understand execution paths.
- Handshake timings include one process start (~constant); do not read them as TLS latency.
- Business-asset numbers (X, Y) in `assets.json` are fictional.

## Sources (all fetched 2026-11-16 unless noted)
- Regulation (EU) 2024/2847 (CRA): https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng ✅
- EC, CRA reporting obligations: https://digital-strategy.ec.europa.eu/en/policies/cra-reporting ✅
- EC, Commission guidance on the CRA (27 Jul 2026): https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation ✅ (announcement)
- EC, CRA standardisation: https://digital-strategy.ec.europa.eu/en/policies/cra-standardisation ✅
- ENISA, Single Reporting Platform: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp ✅
- EC, Post-Quantum Cryptography: https://digital-strategy.ec.europa.eu/en/policies/post-quantum-cryptography ✅
- EU Coordinated Implementation Roadmap for the Transition to PQC (June 2025, PDF): https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography ✅
- NIST IR 8547 (Oct 2026): https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8547.pdf ✅; FIPS 203/204/205 pages: https://csrc.nist.gov/pubs/fips/203/final (also /204, /205) and the [CSRC PQC project page](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post_Quantum_Cryptography-Standardization) 🟠 (abstract pages need JavaScript; dates via search result)
- CISA et al., 2026 Minimum Elements for an SBOM: https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom ✅ (PDF read)
- BSI TR-03183 and Part 2 v2.1.0: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03183/TR-03183_node.html ✅
- RFC 10024: https://www.rfc-editor.org/rfc/rfc10024.html ✅
- OpenSSL 3.5 notes: https://openssl.org/news/openssl-3.5-notes/ 🟠 (search result text); CHANGES.md in the 3.5.0 tag 🟠; our `openssl version` 3.5.7 🧪
- ECMA-424 (CycloneDX 1.7): https://ecma-international.org/publications-and-standards/standards/ecma-424/ ✅
- CycloneDX Authoritative Guide to CBOM: https://cyclonedx.org/guides/OWASP%5FCycloneDX-Authoritative-Guide-to-CBOM-en.pdf 🟠
- CISA KEV catalogue (JSON feed, catalog 2026.11.13, 1781 entries): https://www.cisa.gov/known-exploited-vulnerabilities-catalog ✅ (feed read)
- Secondary: FIPS 206/207 status ([QSECDEF](https://quantumsecuritydefence.com/insights/fips-206-fn-dsa/), [CipherStance](https://cipherstance.com/knowledge/post-quantum-cryptography/nist-post-quantum-standards-explained/)), IR 8547 draft-vs-final comparison ([Applied PQC](https://appliedpqc.io/blog-nist-ir-8547-final.html)), harmonised-standards tracker ([CRA Evidence](https://craevidence.com/cra-compliance/harmonised-standards-status)), sbomqs BSI field mapping 🟠.
