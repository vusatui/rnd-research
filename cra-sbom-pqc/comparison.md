# CRA, SBOM and PQC: approaches and tools compared (as of 2026-11-16)

> **General information, not legal advice.** Legend as in `research.md`: ✅ verified on primary page/standard/our own run, 🟡 vendor claim,
> 🟠 secondary (or primary known through a search summary), ❌ unverified, 🧪 measured in our workshop, 🔮 forecast.
> We **ran** only: syft, grype, osv-scanner, OpenVEX through grype, OpenSSL 3.5.7, and our own scripts. Everything else is described from public documentation and marked as not tested.

## 1. Four questions, four toolboxes

| Question the CRA / PQC work forces | Toolbox | What the law or roadmap actually asks |
|---|---|---|
| What is in my product? | SBOM generation | SBOM, machine-readable, >= top-level deps (Annex I Part II(1)) ✅ |
| Which parts are vulnerable, and does it matter? | Scanning + VEX | handle vulnerabilities without delay, disclose fixed ones, no known exploitable vulnerabilities at market placement (Annex I) ✅ |
| Is something actively exploited, and who do I tell by when? | Reporting runbook + clock | 24 h / 72 h / 14 d / 1 month via SRP (Art. 14) ✅ |
| Where do I use quantum-vulnerable crypto and what do I do first? | Crypto inventory (CBOM) + hybrid pilots | EU roadmap: start by end 2026, high-risk by end 2030 (Member States) ✅; CRA itself: "state of the art" (Annex I Part I(2)(e)) ✅ |

## 2. SBOM generators

| Tool | Approach | Formats | Notes | Evidence |
|---|---|---|---|---|
| **syft** (Anchore) | file-system / image / dir cataloguers (lockfiles, installed packages, binaries) | CycloneDX (1.7 default JSON in v1.57.1), SPDX, own JSON | 72 components for our sample in ~1 s; Python `requirements.txt` gives **only the pinned lines** (no transitive closure); no supplier/creator, no hashes for lockfile packages, no author, no lifecycle; licences for 66/72 | 🧪 |
| **cdxgen** (CycloneDX) | language-aware, can resolve dependency trees (needs build tools) and has a crypto/CBOM mode | CycloneDX | not installed or tested here | ❌ (project docs only) |
| **Trivy** (Aqua) | scanner that also emits SBOMs | CycloneDX, SPDX | not tested | ❌ |
| **Language/build plugins** (CycloneDX Maven/Gradle/npm/pip plugins, Microsoft sbom-tool, ...) | read the build graph - the most accurate for transitive dependencies and hashes of the artefact you ship | CycloneDX / SPDX | not tested; **build-time SBOM is what CISA's "Generation Context" and BSI's "deployable hash" assume** | 🟠 (CISA 2026 PDF ✅ for the generation-context idea) |
| **Hand enrichment** (our `enrich.py`) | add facts you really know: lockfile integrity hashes, author, lifecycle, `compositions` | CycloneDX | BSI per-component coverage 46.6 % -> 67.0 %; creators, supplier, source URIs stay missing | 🧪 |

Decision rule: generate **at build time** from the package manager's resolved graph, keep the SBOM with the release artefact, and run an automated field check (ours or [sbomqs](https://github.com/interlynk-io/sbomqs) 🟠, not tested) in CI. A scan-the-repo SBOM is a starting point.

## 3. Format: CycloneDX vs SPDX
| | CycloneDX | SPDX |
|---|---|---|
| Standard | ECMA-424 (v1.7, 2nd ed. Dec 2025) ✅ | SPDX 3.0.1 required by BSI TR-03183-2 v2.1.0 ✅ |
| BSI TR-03183-2 v2.1.0 | >= 1.6 ✅ | >= 3.0.1 (SPDX 2 no longer allowed) ✅ |
| Vulnerabilities / VEX in the same format | yes (VEX in CycloneDX) ✅ | VEX is separate (OpenVEX/CSAF) 🟠 |
| Crypto assets (CBOM) | native since 1.6 (`cryptographic-asset`) ✅ 🧪 schema-validated | not covered by us ❌ |
| Tool support in our run | syft default, osv/grype read it 🧪 | syft emitted SPDX-2.3 JSON, which BSI v2.1.0 no longer accepts (needs SPDX >= 3.0.1) 🧪 partial |

## 4. Vulnerability scanning and VEX

| Tool | Input | DB | Our result on the sample 🧪 |
|---|---|---|---|
| **grype 0.121.3** | SBOM, dir, image | Anchore DB (built 2026-11-15); includes KEV + EPSS fields in JSON ✅ | **156 findings** in 15 packages (16 crit / 79 high / 50 med / 11 low); fix version known for all; **1 KEV hit** (Pillow 8.1.0, CVE-2023-4863) |
| **osv-scanner 2.7.1** | lockfiles, source, SBOM | OSV.dev | **18 packages / 215 vulns**; resolves transitive Python deps from `requirements.txt` (3 extra packages); network needed |
| **Dependency-Track**, **Trivy**, commercial SCA | ingest SBOMs continuously | various | not tested ❌ / 🟡 |

Overlap: all 228 IDs grype reports also appear in osv-scanner's 416 (aliases included); osv-only extras come from the transitive packages and different alias handling 🧪.

**VEX** (the statement "this CVE does not affect us"):

| Format | How it is consumed | Status in our run |
|---|---|---|
| **OpenVEX** v0.2.0 | `grype --vex file.json` | worked: 19 statements for 6 unused direct dependencies -> 156 -> 137 findings 🧪 |
| CycloneDX VEX (`vulnerabilities[].analysis`) | Dependency-Track, grype (as input) 🟠 | not run ❌ |
| CSAF VEX | advisory ecosystems 🟠 | not run ❌ |

Warning: the VEX we generate is a **claim by the manufacturer built on an import check**; wrong "not affected" statements are a liability in an audit and in a CRA incident. Keep a human sign-off and an expiry/re-evaluation rule.

## 5. Reporting operations (Art. 14)

| Approach | Good for | Weak spot |
|---|---|---|
| **Runbook + clock script** (ours: `cra_clock.py`, `draft.py`) | small teams; pre-fills facts from scan data; deadline arithmetic is tested | does not know your awareness moment; SRP form fields differ from our draft ❌ |
| PSIRT / incident tooling (ticketing with SLA timers) | enterprises with a 24x7 desk | needs the CRA clock modelled (14 days start at the *mitigating measure*; one month after the 72 h notification) |
| Pure manual SRP entry | rare events | 24 h is hard without a prepared template and named account roles ([SRP guidance: authorised representatives, registration](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp) ✅ listed there) |
| LLM drafting | speed for plain-language advisories | 🧪 4 of 4 free-model drafts **inflated severity** ("critical", "remote code execution"); use as an editor's first draft behind a fact guard only |

Triggers to rehearse: KEV listing, vendor advisory "exploited in the wild", own telemetry. Pick the *evidence standard* in advance (research.md section 5).

## 6. Crypto inventory (CBOM)

| Source of truth | What it finds | Misses | In our run |
|---|---|---|---|
| **Source/config grep** (ours, `scan_crypto.py`) | declared use in code and configs, key sizes in literals | libraries' internals, binaries, HSM/KMS, runtime-selected algorithms | 🧪 32 findings / 5 files |
| **Dependency-based** (which crypto libraries ship, from the SBOM) | libraries (OpenSSL, BoringSSL, Bouncy Castle) but not their use | usage | 🟠 idea; not run |
| **Static analysis with CBOM output** (SonarQube crypto rules, CBOMkit, cdxgen crypto mode) | typed crypto assets with call sites | closed-source | not tested ❌ / 🟡 |
| **Network probing** (TLS handshake: group, certificate signature) | what an *outside client* actually sees on endpoints | internal protocols, data at rest | 🧪 ex5 part D: six endpoints classified in one pass |
| **Certificate/key stores, KMS/HSM exports** | key types, validity, owners | usage context | not run |
| **Asset owners' interviews** | data lifetimes, migration constraints (the X and Y of Mosca) | - | 🧪 fictional `assets.json` |

A CBOM without business context is a list; the value is the join with data lifetime and update path. Standard container: CycloneDX 1.6+ (`cryptographic-asset`, `nistQuantumSecurityLevel`) ✅ 🧪.

## 7. PQC migration options

| Option | What changes | Pros | Cons / risks | Evidence |
|---|---|---|---|---|
| **Hybrid key exchange in TLS** (X25519MLKEM768) | client/server library or terminator | RFC 10024 ✅; default in OpenSSL 3.5 ✅ 🧪; Go 1.24 `crypto/tls` enables it by default 🟠 ([release notes](https://go.dev/doc/go1.24)); JDK TLS hybrid targeted for JDK 27 per JEP 527 🟠 (status not verified) | +1.2 kB ClientHello, +1.1 kB server flight 🧪; middleboxes that choke on large ClientHellos (not tested ❌); client-only change gives nothing if the server is classical (falls back) 🧪 | mostly ✅ |
| **Pure ML-KEM** (MLKEM768) | groups must be enabled explicitly | smaller than hybrid (1474 B ClientHello 🧪) | OpenSSL 3.5 **default server rejects it** 🧪; NIST/EU say hybrids are the transition tool ✅ | ✅ 🧪 |
| **PQ signatures (ML-DSA, SLH-DSA)** for code signing, firmware, PKI | keys, certificates, verifiers in devices | ML-DSA works in OpenSSL 3.5.7 TLS 1.3 🧪 | certificate 3.9-7.5 kB vs 0.4 kB (ECDSA) 🧪; ecosystem (public CAs, browsers, HSMs) not tested ❌; FN-DSA (FIPS 206) unpublished ✅ | 🧪 / ❌ |
| **Crypto-agility first** (algorithm negotiation, versioned formats, key rotation) | architecture | makes every later step cheaper; named in the EU roadmap as a goal ✅ | no direct security gain | ✅ |
| **Symmetric / PSK designs** for closed systems | protocol redesign | EU roadmap notes alternatives such as symmetric methods ✅ | key distribution burden | ✅ (mention only) |
| **Wait** | nothing | no cost today | harvest-now-decrypt-later exposure for long-lived secrets; IR 8547 dates (2030/2035) ✅ | ✅ |

## 8. Decision guide
1. Reporting first (it is the dated legal duty): named people, SRP accounts, a template, the clock tested in a drill. 
2. SBOM from the **build**, validated against BSI/CISA fields in CI, with an explicit statement of coverage (CISA "Coverage", "Explicitly Identifying Unknown Information").
3. Scan with two engines; triage with VEX **only** with human sign-off; tie KEV/EPSS to reporting evidence.
4. Crypto inventory: code + dependencies + network probe, joined with data lifetimes; run the ranking at several Z values.
5. Pilot **hybrid TLS** on one endpoint you control, measure bytes and failures, keep a classical fallback, then widen.
6. Put long-lived signing roots and non-updatable devices at the top of the signature backlog; do not wait for FN-DSA.
