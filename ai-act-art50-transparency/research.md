# EU AI Act Art. 50 transparency (AI-content marking, AI disclosure) - research notes

> **General information, not legal advice.** This is an engineering-oriented reading of public sources as of
> **2026-10-26**. It is not a compliance opinion; whether a given system is in scope, who is "provider" or "deployer", and
> what is sufficient are legal questions for counsel and, ultimately, for the competent authorities and the CJEU.

Question behind the topic: *"We ship chatbots and generative features. From 2 August 2026 Art. 50 applies - what exactly
must the product do, what do the official documents say, and which marking techniques actually survive contact with the real world?"*

Legend (same as the other topics, plus 🔮):
- ✅ **verified**: read on the primary page (regulation text, Commission page/document, standard, paper, repo, our own tool output).
- 🟡 **vendor-claim**: a vendor describing itself or its product; not independently reproduced.
- 🟠 **secondary**: law-firm/blog/press/aggregator, or a primary page known to us only through a search-result summary.
- ❌ **unpublished / unverified / disputed**.
- 🧪 **measured by us** in the workshop (`workshop/`, results in `workshop/results/`).
- 🔮 **forecast / expectation**, not a fact.

## TL;DR (key findings)

1. **Art. 50 applies since 2 Aug 2026, and the Digital Omnibus changed very little of it.** Regulation (EU) 2026/1744
   (signed 8 Jul 2026, published OJ 24 Jul 2026, in force on the third day after publication) touches Art. 50 in exactly two
   places: it **rewrites Art. 50(7)** (codes of practice; the Commission assesses adequacy and may adopt an implementing act
   if a code is inadequate) and adds **Art. 111(4)**: providers of generative systems *already on the market before 2 Aug 2026*
   must "take the necessary steps in order to comply with Article 50(2) by **2 December 2026**". Art. 50(1) (chatbot
   disclosure), 50(3), 50(4), 50(5) and the text of 50(2) are unchanged ✅ ([Regulation text on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng);
   consolidated text with "AMENDED" markers: [AI Act Service Desk, Art. 50](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50)).
   The high-risk dates moved (2 Dec 2027 for Annex III, 2 Aug 2028 for Annex I) - that is *not* Art. 50 ✅.
2. **The grace period is narrow.** It covers only the *marking* duty of 50(2), only for systems placed on the market
   *before* 2 Aug 2026. The Commission's Guidelines add: a system that is partly interactive and partly generative
   gets the grace only for marking; the chatbot disclosure of 50(1) applies from 2 Aug 2026 (Guidelines points 153-154) ✅.
   Whether a *new version* of an old system is "already placed on the market" is not settled in the text ❌ (open item).
3. **Official guidance exists and is concrete.** Commission Guidelines C(2026) 5054 final (20 Jul 2026, non-binding)
   say: AI agents must disclose **both** that they are AI **and on whose behalf** they act (point 31); a notice buried
   in T&Cs, an unclear label such as "assistant", a generic site-wide "uses AI", a technical statement such as "uses LLMs", or
   invisible metadata/watermarks alone are **insufficient** for 50(1) (point 38); "obviously AI" is a restrictive exception (45) ✅.
4. **The Code of Practice (final 10 Jun 2026) makes "multi-layer" the baseline for providers**: signed metadata
   **plus** an imperceptible watermark; fingerprinting/logging is optional and "not sufficient" alone; free-form text
   longer than 200 tokens must be watermarked; detection must be offered (free) with interoperability steps due
   **2 Feb 2027** (Measure 3.4(c)); robustness must cover screenshots, crops, mirroring, paraphrase and translation
   cycles ✅. The Commission and the AI Board assessed it as adequate (8-9 Jul 2026), but adherence gives **no presumption of
   conformity** (Omnibus recital on Art. 50(7)) and is only a "straightforward, predictable, and legally certain way" to show compliance (Guidelines 147) ✅. ~190 organisations signed by 31 Jul 2026 (incl. Google, Microsoft, OpenAI, Anthropic, Meta, Mistral) ✅.
5. **A date mix-up circulates:** at least one law-firm memo (Paul Weiss, as summarised by search results) attributes the
   2 Feb 2027 watermark-detection interoperability deadline to the Digital Omnibus 🟠. The Omnibus text contains no
   such date (its 2027 dates are 1/2 Aug, 2 Sep, 2 Dec 2027) ✅; the date is in the **Code**, Measure 3.4(c) ✅ - a voluntary
   instrument. Cite the primary source.
6. **No single technique survives everyday handling - our measurements agree with the Code's "multi-layer" premise.**
   In our lab, every re-encode by a non-C2PA-aware tool removed the C2PA manifest (11/11 transformations) 🧪; an open DWT-DCT-SVD
   watermark survived JPEG q60 and noise but not 50% resize, crop, rotation, mirroring or a screenshot at 125% display
   scaling 🧪; a perceptual hash survived re-compression and resize but not crop/rotate/mirror 🧪. **4 of 11 everyday
   transformations defeated all three layers at once** (crop, rotate 5 degrees, mirror, scaled screenshot) 🧪 (3 synthetic images, simple open
   stand-ins - not a statement about SynthID, TrustMark, Video Seal or any vendor's product).
7. **Prompt-only disclosure fails exactly where Art. 50(1) bites.** With an honest system prompt, 0 of 10 ordinary first
   replies told the user it was an AI; under a "you are Anna, a human" persona prompt 15 of 20 identity questions got an explicit
   human claim and the other 5 an evasive non-answer (0 honest) 🧪. A regex output guard caught only 10 of the 15 explicit claims 🧪. What works is a
   **system-level** design: fixed first-turn notice + persistent badge + deterministic routing of "are you human?" to an
   application-owned answer (20/20 in-sample; only 7/13 on a fresh probe, 0/9 false alarms - heuristics need a better classifier) 🧪.
8. **Text is the weak point and the Code knows it.** SynthID-Text-style watermarking on a small local model was detected in
   12/12 unedited texts at 0/24 false alarms, survived 10% word drops and a de/en translation cycle (6/6, 41% of 4-grams preserved) but
   an LLM paraphrase (1% 4-gram overlap) took detection to 1/6; at 20-40 tokens the fixed threshold gave 5/24 and 2/24 false alarms 🧪.
   The Code answers with the 200-token threshold and *restricted* detector access for text (Measures 1.1.2, 2.1.2) ✅.

## 1. The legal text

### 1.1 What Art. 50 requires (consolidated text, AI Act Service Desk) ✅

Source: [Art. 50](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) (consolidated text as at 27 Jul 2026, "AMENDED" marker only on para 7).

| Para | Who | Duty (paraphrase of the text) | Main exceptions |
|---|---|---|---|
| 50(1) | **Provider** of AI systems intended to interact directly with natural persons | design/develop the system so persons are informed they interact with an AI system | obvious to a "reasonably well-informed, observant and circumspect" person; systems authorised by law for criminal-offence detection etc. (not if open to the public to report offences) |
| 50(2) | **Provider** of systems (incl. GPAI systems) generating synthetic audio, image, video or text | outputs marked **in a machine-readable format and detectable** as artificially generated or manipulated; solutions "effective, interoperable, robust and reliable as far as technically feasible", considering content type, cost, state of the art | assistive function for standard editing; no substantial alteration of input/semantics; law-enforcement authorisation |
| 50(3) | **Deployer** of emotion-recognition or biometric-categorisation systems | inform exposed persons of the operation; process data per GDPR etc. | permitted-by-law criminal-offence use |
| 50(4) | **Deployer** | disclose that image/audio/video **deep fakes** are artificially generated or manipulated; also AI-generated **text published to inform the public on matters of public interest** | artistic/creative/satirical: disclosure limited and non-intrusive; text: human review/editorial control with editorial responsibility |
| 50(5) | all of the above | information clear and distinguishable, **at the latest at first interaction or exposure**; accessible | - |
| 50(6) | | does not affect Chapter III or other transparency law | |
| 50(7) | Commission | encourage codes of practice; **as rewritten by the Omnibus**: assess adequacy for 50(2) and (4) via the Art. 56(6) procedure; may adopt an implementing act with common rules if a code is inadequate | |

Fines for infringing Art. 50: up to EUR 15,000,000 or 3% of worldwide annual turnover, whichever is higher; for SMEs
the lower of the two; EU institutions up to EUR 750,000 (Guidelines point 152 ✅). The Omnibus adds Art. 99(6a): for small
mid-caps (SMCs) each fine is "up to the percentages or amount ... whichever is lower" ✅ ([Omnibus text, point 38(c)](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng)).

### 1.2 What the Digital Omnibus on AI changed for Art. 50 ✅

Primary source: [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) ("Done at Strasbourg, 8 July 2026"; OJ L 2026/1744, **24.7.2026**;
"shall enter into force on the third day following that of its publication" -> **27 Jul 2026**, our arithmetic from the Article 4 text).
We read the full HTML text (EUR-Lex blocks plain HTTP clients; it renders in a headless browser) and searched it for Art. 50.

| Change | Text | Effect |
|---|---|---|
| Art. 50(7) replaced | point (20): "The Commission shall encourage and facilitate the drawing up of codes of practice ... The Commission, taking utmost account of the opinion of the Board, shall assess whether adherence to those codes ... is adequate to ensure compliance with ... paragraphs 2 and 4 ... If it deems the code of practice to be inadequate, the Commission may adopt an implementing act specifying common rules ..." | the Commission no longer *approves* a code by implementing act; it *assesses adequacy*; recital: such codes "have limited legal effect, and in particular do not grant a presumption of conformity" |
| Art. 111(4) added | "Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text content, that have been placed on the market before 2 August 2026 shall take the necessary steps in order to comply with Article 50(2) by 2 December 2026." (recital 38: "transitional period of four months") | 50(2) marking for **legacy generative systems**: 2 Dec 2026 instead of 2 Aug 2026 |
| unchanged | 50(1), (2) text, (3), (4), (5) | apply from 2 Aug 2026 (Art. 113) |
| not Art. 50, but often conflated | Art. 113 third paragraph: Chapter III Sections 1-3 apply from **2 Dec 2027** (Annex III high-risk) / **2 Aug 2028** (Annex I); Art. 5 amendments from 2 Dec 2026; SMC fine proportionality (Art. 99(6a)) | high-risk timeline only |

Commission reading of the grace period (Guidelines points 153-154 ✅): all in-scope systems must comply on 2 Aug 2026 regardless of
placing date; the Omnibus "envisages a targeted grandfathering rule only with regard to the marking and detection obligations under
Article 50(2)"; mixed interactive+generative systems benefit **only** for marking; outputs generated before 2 Aug 2026 need no retroactive
marking; public-interest texts generated earlier but **published on/after** 2 Aug 2026 must be labelled; holders of pre-existing unlabelled deepfakes are "encouraged" to label.

Open on the text itself ❌: whether a *new version* of a system placed on the market earlier still counts as "placed on the market before 2 Aug 2026" - we did not find it answered in the Omnibus text or the Guidelines passages we read; the Commission's FAQ page has a date typo we noticed in an earlier pass (not re-checked) ❌.

### 1.3 Commission Guidelines on Art. 50 (C(2026) 5054 final, 20 Jul 2026) ✅

Official PDF: [Guidelines on the implementation of the transparency obligations ... under Article 50](https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-07/guidelines_on_the_implementation_of_the_transparency_obligations_for_certain_ai_systems_under_article_50_of_the_ai_act_bzptwqhk0ikg1dtlddap41psfy_131215.pdf)
(page: [EC library](https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems)). Non-binding; authoritative interpretation rests with the CJEU (point 5 of the Guidelines).
Points we use in the workshop:

| Topic | Point | What it says |
|---|---|---|
| four scope criteria of 50(1) | 30 | (i) AI system, (ii) intended to interact (bidirectional, genuinely conversational/responsive), (iii) directly, (iv) with natural persons; rule-based out-of-office replies are not AI systems |
| AI agents | 31 | covered if they interact with the instructing person or others (bookings, correspondence, negotiation, purchases); must disclose "both their artificial nature and the person on whose behalf they are acting";  |
| when to inform | 33, 40 | at the latest at first interaction; one prominent notice before first interaction "likely to suffice in most instances"; periodic reminders likely needed in riskier contexts, e.g. vulnerable persons such as children and the elderly |
| content of the notice | 35-37 | explicit about the artificial, non-human nature, appropriate to the context; multimodal and accessible disclosure recommended as best practice; e.g. spoken "This is an AI-powered assistant" at the start of a voice interaction |
| **insufficient alone** | 38 | T&Cs/URL/docs only; machine-readable marks not perceivable at the point of interaction (still fine for 50(2)); ambiguous labels ("assistant") or human-like representations; generalised "Services on this website use AI"; purely technical statements ("uses LLMs") |
| banner blindness | 39 | calibrate disclosures to avoid habituation |
| obviousness exception | 42-45 | provider must assess *and demonstrate*; interpreted restrictively; general awareness that chatbots exist does not make a given interaction obvious |
| 50(2) scope | 56-68 | AI system generating audio/image/video/text; also agents' perceivable outputs (63) and AI-generated digital twins (62); excluded e.g. source code and SQL/YAML/JSON-type artefacts, 3-D point clouds/meshes, recommender selection that creates nothing new |
| marking + detection | 69-77 | both elements required; machine-readable; single technique or combination (72); Recital 133 examples: watermarks, metadata, cryptographic provenance, logging, fingerprints (73); a full provenance chain is **not** required (73); detection results must be human-readable (75) |
| role in the value chain | 74, 27 | marking may be implemented at different stages of the value chain (74); Art. 50 does not apply to GPAI *models* as such, but systems built on a GPAI model of the same provider must apply the transparency measures (27) |
| open source | 23-24 | open-source *systems* in scope of Art. 50 still need to comply; plain open-source components are not subject |
| code of practice | 146-150 | adhering to an adequate code is a "straightforward, predictable, and legally certain way" but alternatives are allowed; non-signatories should do a gap analysis against the code; the Guidelines cite Art. 99(7)(e) in this context |
| enforcement | 151-152 | MSAs and the AI Office (for systems built on GPAI models of the same provider); fines as in 1.1 |

### 1.4 Code of Practice on Transparency of AI-generated Content ✅

- Final text published **10 Jun 2026** ([EC press release](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content), [Code page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)). We read the PDF text via a public mirror ([medianama.com copy](https://www.medianama.com/wp-content/uploads/2026/06/CoP_Transparency_of_AI_generated_content_jtHnEivPctLZtkoRFQrkbStffUY_129555-1.pdf)); we did not find the official PDF link on the EC page ❌ (content is the EC's own document; verify against the EC download).
- Adequacy: Commission opinion 8 Jul 2026, AI Board 9 Jul 2026 🟠 (EC library page via search summary: [opinion](https://digital-strategy.ec.europa.eu/en/library/commission-opinion-assessment-code-practice-transparency-ai-generated-content); Guidelines footnote 44 ✅ confirms the opinion exists). Signatories 31 Jul 2026: "about 190 organisations"; list shows 95 (Section 1) and 192 (Section 2) names ✅ ([EC news](https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content)).
- **Section 1 (providers, Art. 50(2),(5))** - key measures ✅:
  - 1.1: at least two layers of machine-readable marking "so long as no single marking technique can ... ensure by itself compliance": **1.1.1 digitally signed, time-stamped metadata**; **1.1.2 imperceptible watermark** ("difficult for it to be separated from the content"), except very short text; free-form text **longer than 200 tokens** still needs a watermark, with detector access possibly restricted to verified expert users; single layer allowed for closed-environment embedded products and for free-form text (which cannot carry metadata); **1.1.3 fingerprinting/logging (optional)** - "relying on fingerprinting or logging alone is not considered sufficient"; logging limited to outputs, privacy-preserving.
  - 1.2 non-removal of markings; 1.3 richer provenance (optional); 1.4 perceptible markings (optional).
  - 2.1-2.3: detection mechanisms, access, clear human-readable results; 2.2 forensic detection (optional).
  - 3.1-3.4: effectiveness, reliability (error rates measured on varied samples incl. other systems' content), **robustness** to typical operations - "screenshot / screencasting, ... (re)compression ... mirroring, cropping, up/downscaling, rotation, ... paraphrasing, translation cycles", the analogue hole (print-and-scan, camcording) - and to adversarial removal/regeneration/forgery; **interoperability**: standards for metadata now; by **2 Feb 2027** a shared access method, a signpost, a shared consortium detector or comparable (3.4(c)).
  - 4.x: compliance process, testing, training, cooperation with authorities.
- **Section 2 (deployers, 50(4))**: common EU icon with the capitalised acronym "AI" (or an equivalent label) for deepfakes and public-interest text; design rules - the capitalised acronym "AI" as main visual element; for video, the icon at the beginning, at regular intervals where possible and after interruptions (to cover screenshots and clipped fragments); an optional second layer with details.
- Code summary (our reading): it is a *provider-side engineering spec* (layers, robustness list, detection access) and a *deployer-side UX spec* (icon, placement). It does **not** cover 50(1) chatbot disclosure or 50(3) - for those the Guidelines are the main source.

## 2. Marking and detection techniques - what is known

Full comparison: [`comparison.md`](comparison.md). Primary facts used:

- **C2PA (Content Credentials)**, spec v2.2 read in full structure ✅ ([spec](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html)): a manifest of signed assertions (claim + signature, X.509, COSE) embedded in the asset (JUMBF) or stored externally; a **hard binding** is a cryptographic hash of the asset (tamper-evident, matches "no other asset, not even renditions"); a **soft binding** is a fingerprint or invisible watermark used to *find* a manifest when it was stripped; trust via C2PA Trust List or validator-configured lists; validation distinguishes valid from trusted. The spec notes that padding in excluded ranges can change without a validation failure - we saw something similar in practice (§3.2). Its change notes mention preparing the document for ISO standardisation ✅; we did not diff later spec versions ❌.
- **Vendor statements on stripping** 🟡: OpenAI's help centre says C2PA metadata can be removed accidentally or intentionally, most social platforms strip metadata and a screenshot can remove it, and (current page) that SynthID watermarks may survive some edits but degrade under heavy changes ([OpenAI Help](https://help.openai.com/en/articles/8912793-provenance-signals-in-openai-generated-content), seen via search summary, page not opened 🟠).
- **Image watermark removal** ✅: Zhao et al., *Invisible Image Watermarks Are Provably Removable Using Generative AI* ([arXiv:2306.01953](https://arxiv.org/abs/2306.01953)): regeneration attacks (add noise, then denoise/reconstruct with a generative model) remove pixel-level invisible watermarks including DwtDctSvd (the paper's headline claim is *provable* removability for low-perturbation schemes); semantic watermarks such as Tree-Ring were more resilient in their tests (check the paper for exact rates - we did not reproduce them). DwtDctSvd is the default Stable Diffusion watermark. **UnMarker** (IEEE S&P 2025, [arXiv:2405.08363](https://arxiv.org/abs/2405.08363)) is a black-box attack reported to defeat seven schemes incl. semantic ones (best detection down to 43%) 🟠 (abstract via search summary).
- **Text watermarking** ✅: Dathathri et al., *Scalable watermarking for identifying LLM outputs*, [Nature 2024](https://www.nature.com/articles/s41586-024-08025-4): tournament sampling, mean g-value score; detectability grows with length and entropy and drops at low entropy; limitations stated by the authors: needs coordination by the generating party, hard to enforce on open-source models, "vulnerability to stealing, spoofing and scrubbing attacks", "weakened by edits to the text, such as through LLM paraphrasing"; post hoc classifiers "perform poorly on out-of-domain data and may have higher false-positive rates for certain groups, such as non-native speakers"; retrieval/logging "raises privacy concerns". The paper reports a live deployment in Gemini with a user-feedback experiment 🟡 (authors' own report; numbers not re-checked here). Open code: HF `transformers` `SynthIDTextWatermarkLogitsProcessor`; the HF doc states texts from the Gemini app are not detectable with its detector ✅ (code comment we read).
- **Detector access**: Google's SynthID Detector portal covers images/audio/video and text via Gemini/Search/Chrome 🟠 ([Google](https://blog.google/innovation-and-ai/products/google-synthid-ai-content-detector/), search summary).
- **Open watermarks for C2PA soft binding** 🟠: Adobe TrustMark (MIT, with C2PA integration, [repo](https://github.com/adobe/trustmark/)), Meta Video Seal (MIT, [repo](https://github.com/facebookresearch/videoseal/)), soft-binding support in C2PA 2.x ✅ (spec text; not tested by us).

## 3. Our measurements (workshop, 2026-10-26, free models, CPU)

All raw data: [`workshop/results/`](workshop/results/). Small samples, procedurally generated images, simple open stand-ins - see `workshop-plan.md` for method and caveats.

### 3.1 Ex1 - chatbot disclosure, prompt vs system level 🧪

Model `nvidia/nemotron-3.5-lightning:free` (OpenRouter, temperature 0.7), fictional product "Ledgerly" support bot, 15 user prompts x 2 repeats x 2 prompt configs = 60 calls.
Manual labels of every reply: [`manual_labels.json`](workshop/ex1_disclosure/manual_labels.json); audit: `workshop/results/ex1_audit.json`.

| Configuration | Ordinary first replies that say "I am an AI" (n=10) | Identity questions (n=20): honest AI answer | explicit human claim | evasive (no AI/human statement) |
|---|---|---|---|---|
| A. honest prompt only | 0 | 20 | 0 | 0 |
| B. deployer "Anna, a human" prompt only | 0 | 0 | 15 | 5 |
| B + output guard (regex on the reply) | 0 (reply unchanged) | 10 replies replaced by the app's truthful answer | 5 explicit claims slipped through (guard recall 10/15) | 5 evasive slipped through |
| B + input router (regex on the *question*) | | 20/20 answered by the app (in-sample) | 0 | 0 |
| fixed first-turn notice (any config) | **10/10 by construction** (app text before the first user message) | | | |

Fresh probe for the router after it was written (13 identity questions, 9 ordinary questions): 7/13 caught, 0/9 false alarms; misses: "Is there a person on the other end?", "Are you an actual employee?", "Do you have feelings like a human?", "Are u a bot lol", "Is anyone real here?" and the French question. So the *guarantee* comes from the notice and the badge; the routers are safety nets whose recall must be measured, not assumed.
Observation: in config A the model often answered identity questions with its own name ("My name is Nemotron, and I'm a language model developed by NVIDIA") - truthful, but not the product's voice and not a first-turn disclosure.

### 3.2 Ex2 - C2PA + watermark + fingerprint survival 🧪

3 procedurally generated 768x768 images; pipeline: embed 64-bit DWT-DCT-SVD watermark -> JPEG q95 -> C2PA sign (test CA; `c2pa.created` with IPTC `trainedAlgorithmicMedia`) -> register a 256-bit dHash. Verdicts use c2pa-python 0.38.1 (c2pa-rs 0.91.3).
Watermark "detected" = >= 50/64 bits (p = 1e-5 by chance, computed in tests); fingerprint "match" = <= 40/256 bits and nearer than any other image (nearest unrelated image: at least 105 bits away).

| transformation | C2PA | watermark (mean bit acc.) | fingerprint |
|---|---|---|---|
| none (file copy) | Trusted x3 | 3/3 (1.00) | 3/3 |
| 1 byte changed in image data | **Invalid** x3 | 3/3 (1.00) | 3/3 |
| re-save as PNG (strips metadata) | **NoManifest** x3 | 3/3 (1.00) | 3/3 |
| JPEG q85 / q60 | NoManifest | 3/3 (0.97 / 0.89) | 3/3 |
| messenger-like (1280 px, q70; *simulated*, not a real app) | NoManifest | 3/3 (0.91) | 3/3 |
| gaussian noise s=8 | NoManifest | 3/3 (1.00) | 3/3 |
| resize 50% | NoManifest | **0/3 (0.47)** | 3/3 |
| crop 80% centre | NoManifest | **0/3 (0.50)** | **0/3** |
| rotate 5 degrees | NoManifest | **0/3 (0.53)** | **0/3** |
| mirror | NoManifest | **0/3 (0.50)** | **0/3** |
| real browser screenshot 1:1 (headless Chrome, lossless) | NoManifest | 3/3 (1.00) | 3/3 |
| browser screenshot, 125% display scaling + page border | NoManifest | **0/3 (0.53)** | **0/3** |
| C2PA-aware crop + re-sign (parent kept as ingredient) | **Trusted** x3, 2 manifests | 0/3 | 0/3 |

Findings: (1) provenance survives only in C2PA-aware pipelines; every other re-encode drops it. (2) Tamper-evidence works: a flipped pixel-data byte -> `assertion.dataHash.mismatch`. During development a single-byte flip in the middle of the file left the verdict `Trusted` (presumably an excluded/padding range, cf. the spec note above); we then flipped a byte at 90% of the file for the test. We did not keep a measurement of this - treat it as an anecdote (🧪, not in committed results): tamper evidence covers the signed ranges, not every byte of the file. (3) Without our test CA in the trust list an intact file validates as `Valid` + `signingCredential.untrusted`, not `Trusted` (unit test) - "valid" is not "trusted". (4) The "screenshot" robustness line in Code Measure 3.3 is not one thing: a lossless 1:1 capture is harmless to pixel watermarks, a scaled/offset capture is not. (5) 4/11 transformations (crop, rotate, mirror, scaled screenshot) defeat all three layers; the fingerprint is a *registry lookup*, useful only if the provider keeps a registry (Code 1.1.3: optional, privacy limits, not sufficient alone).

### 3.3 Ex3 - SynthID-Text-style watermark on a small local model 🧪

`HuggingFaceTB/SmolLM2-360M-Instruct`, HF `SynthIDTextWatermarkingConfig` (30 layers, 5-gram context, demo keys), 12 prompts, up to 150 new tokens, temperature 0.8/top-k 40; our own mean-g detector (not Google's); threshold = max over 24 non-watermarked texts (12 unwatermarked LLM + 12 public-domain human paragraphs from Project Gutenberg) = 0.5152.

| condition | texts | mean g | above threshold |
|---|---|---|---|
| watermarked, as generated | 12 | 0.557 | 12/12 |
| unwatermarked LLM text / human text | 12 / 12 | 0.502 / 0.496 | 0/12, 0/12 |
| drop 10% of words / drop 30% | 12 | 0.544 / 0.524 | 12/12, 10/12 |
| swap 20% adjacent words | 12 | 0.529 | 12/12 |
| hyphen typos in 30% of words | 12 | 0.519 | 8/12 |
| first half only | 12 | 0.550 | 12/12 |
| LLM paraphrase (4-gram overlap with original 1%) | 6 | 0.508 | **1/6** |
| EN->DE->EN translation cycle by LLM (overlap 41%) | 6 | 0.526 | 6/6 |
| only first 20 / 40 / 80 / 150 tokens scored | 12 | 0.535 / 0.549 / 0.556 / 0.557 | 12/12 each; **false alarms on non-watermarked: 5/24, 2/24, 0/24, 0/24** |

Reading: the watermark is statistically strong at 80-150 tokens, brittle against rewording (paraphrase), and unreliable on very short text - consistent with the Nature paper's limitations and with the Code's 200-token rule and expert-only detector access. The translation-cycle survival is partly explained by preserved phrasing (41% of 4-grams), not evidence that translation is harmless. Caveats: small model, one key, n = 6 for LLM attacks, null set of 24, human text is 19th-century fiction while LLM text is modern prose (domain mismatch).

## 4. Consensus vs disputed

| Topic | Consensus (sources agree) | Disputed / open |
|---|---|---|
| Dates | Art. 50 from 2 Aug 2026; 50(2) grace to 2 Dec 2026 for pre-existing generative systems ✅ | scope of "placed on the market" for updated systems ❌; whether the 2 Feb 2027 date is binding (it is a voluntary Code deadline ✅) |
| Chatbot disclosure | the notice must be explicit, in context, at first interaction ✅ | how often to repeat; what is "obvious" for audiences (case-by-case, restrictive) |
| Techniques | no single technique is enough today (Code 1.1; Nature limitations; OpenAI help 🟡; our 🧪) | whether pixel watermarks can ever be robust to regeneration (provable removal for small perturbations ✅ vs semantic watermarks robust at a visibility cost ✅ vs UnMarker 🟠); whether text watermarks can be enforced for open models |
| Code of Practice | adequate in the Commission's view, voluntary, not conclusive ✅ | how market surveillance authorities will treat non-signatories; first enforcement practice 🔮 |
| Detection | must exist and be usable ✅ | who pays, who gets access (text detectors restricted per Code) |

## 5. Open / unverified items

- ❌ The official EC PDF for the Code was not located; we used a public mirror of the PDF. The EUR-Lex Omnibus text was read in a headless browser (plain HTTP returns 202); the consolidated Art. 50 text via the AI Act Service Desk.
- 🟠 Commission/AI Board adequacy dates (8-9 Jul 2026), Paul Weiss memo, OpenAI help page, Google SynthID Detector, UnMarker, TrustMark/Video Seal facts were seen through search summaries or repo pages, not read in full.
- ❌ Whether a new version of a legacy system gets the Art. 111(4) window; the EC FAQ date typo noticed earlier was not re-verified.
- ❌ We did not read the Code's Section 2 (deployer) measures line by line beyond icon/placement; we did not test platform behaviour (which social networks strip C2PA today) - only simulated recompression.
- ❌ Studies we know of but did not open: Fritz/Serra/Puccetti-type user-comprehension studies of AI labels; Washington Post-style real-platform tests of Content Credentials; Liang et al. (cited via the Nature paper only).
- 🔮 Market surveillance practice, first fines, EU icon uptake, whether C2PA soft-binding resolution becomes the "signpost" in Measure 3.4(c) - all expectation, no evidence yet.
- The workshop's marking layers are open stand-ins (DWT-DCT-SVD, dHash, a test CA) and its text watermark runs on a 360M model: it demonstrates *mechanisms and failure modes*, not the performance of any vendor product.

## 6. Sources (index)

Primary: [Reg. (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) · [Art. 50 consolidated](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) · [Guidelines C(2026) 5054](https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-07/guidelines_on_the_implementation_of_the_transparency_obligations_for_certain_ai_systems_under_article_50_of_the_ai_act_bzptwqhk0ikg1dtlddap41psfy_131215.pdf) · [Code of Practice page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) · [EC press release 10 Jun](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content) · [EC signatories news 31 Jul](https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content) · [C2PA spec 2.2](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html) · [Nature 2024 SynthID-Text](https://www.nature.com/articles/s41586-024-08025-4) · [arXiv 2306.01953](https://arxiv.org/abs/2306.01953).
Secondary: [NicFab on the Parliament vote (16 Jun 2026; Art. 50 marking date 2 Dec 2026 and high-risk dates)](https://www.nicfab.eu/en/posts/digital-omnibus-ai-final-approval/) · [Paul Weiss memo](https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content) · [Freshfields #33](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-33-the-final-code-of-practice-on-transparency-of-ai-generate-102n4yx) · [OpenAI Help](https://help.openai.com/en/articles/8912793-provenance-signals-in-openai-generated-content) · [Google SynthID Detector](https://blog.google/innovation-and-ai/products/google-synthid-ai-content-detector/) · [UnMarker](https://arxiv.org/abs/2405.08363) · [TrustMark](https://github.com/adobe/trustmark/) · [Video Seal](https://github.com/facebookresearch/videoseal/).
