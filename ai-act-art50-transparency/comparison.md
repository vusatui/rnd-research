# Marking and detection techniques for AI-generated content (as of 2026-10-26)

> **General information, not legal advice.** Legend as in `research.md`: ✅ verified on primary page/paper/spec, 🟡 vendor claim,
> 🟠 secondary (or primary known through a search summary), ❌ unverified/unpublished, 🧪 measured in our workshop, 🔮 forecast.

Art. 50(2) requires outputs of generative systems to be "marked in a machine-readable format and detectable", with solutions
"effective, interoperable, robust and reliable as far as technically feasible" ✅. The Guidelines accept any single technique
or a combination (point 72-73) ✅; the voluntary Code of Practice asks providers for **two layers** (signed metadata + imperceptible
watermark), fingerprinting/logging as an optional third, and detection with interoperability steps due 2 Feb 2027 ✅.

## 1. Technique matrix

| Technique | What it gives | How it is lost | Interop / standards | Code of Practice (final, Jun 2026) | Our measurement 🧪 |
|---|---|---|---|---|---|
| **C2PA Content Credentials** (signed manifest, hard binding to the asset hash) | Who/what made or edited the asset; tamper evidence; edit history through "ingredients" ✅ [spec 2.2](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html) | Any re-encode/screenshot/platform upload by a tool that does not carry the manifest. Vendors say the same 🟡 [OpenAI help](https://help.openai.com/en/articles/8912793-provenance-signals-in-openai-generated-content) | Open spec, trust lists, signed with X.509 certificates; "valid" is not "trusted" (needs a trusted signer) ✅ | Measure 1.1.1: signed, time-stamped metadata is the first required layer ✅ | Trusted when untouched; **dropped by 11/11** non-C2PA transformations; 1 changed pixel byte -> Invalid; a C2PA-aware crop+re-sign keeps a 2-manifest chain |
| **Unsigned metadata** (EXIF/XMP/IPTC `digitalSourceType`, PNG text chunks) | Cheap hint; IPTC vocabulary reused by C2PA actions ✅ | Trivially edited or stripped; forgeable (no signature) | Several vocabularies; no signature, so no trust model | Not sufficient by itself: Measure 1.1.1 requires *digitally signed* metadata ✅ | not tested separately (our C2PA-less re-saves drop all embedded metadata we wrote) |
| **Invisible image watermark - open classical** (DWT-DCT-SVD, the Stable Diffusion default) | Survives mild pixel-level processing; no manifest needed | Geometric changes (resize/crop/rotate/mirror), regeneration attacks ✅ [arXiv:2306.01953](https://arxiv.org/abs/2306.01953) | Not interoperable (private payload/key); fine as a teaching stand-in | Measure 1.1.2 requires an imperceptible watermark that is hard to separate; robustness list in 3.3 ✅ | 64 bits, 3 images: survived JPEG q60 (0.89 bit acc.), noise, 1:1 screenshot; **0/3** after 50% resize, 80% crop, 5-deg rotation, mirror, 125% screenshot |
| **Invisible image/video/audio watermark - learned/commercial** (Google SynthID, Adobe TrustMark, Meta Video Seal / AudioSeal) | Designed for robustness to compression and edits; payload can point at a manifest (soft binding) | Strong edits, regeneration/diffusion "UnMarker"-style attacks 🟠 [arXiv:2405.08363](https://arxiv.org/abs/2405.08363); detectors may be closed or per-vendor | TrustMark and Video Seal are open-source (MIT) 🟠 [TrustMark](https://github.com/adobe/trustmark/), [Video Seal](https://github.com/facebookresearch/videoseal/); SynthID detector portal is Google's 🟠 | Section 1 signatories include Google, Meta, Microsoft, OpenAI, Black Forest Labs ✅ | not tested (no open reproducible model used; we make no claim about these products) |
| **Semantic / latent watermark** (e.g. Tree-Ring) | Embedded in the generation process, more resilient to pixel edits in the authors' tests ✅ [arXiv:2306.01953](https://arxiv.org/abs/2306.01953) | Needs access to generator/inversion; attacks reported against semantic marks too 🟠 | Research-grade | - | not tested |
| **Text watermark** (SynthID-Text: tournament sampling, keyed g-values) | Detectable statistically without changing quality much per the authors ✅ [Nature](https://www.nature.com/articles/s41586-024-08025-4) | Paraphrase, heavy editing; short or low-entropy text; steal/spoof/scrub; cannot be enforced on open models | HF open implementation; detector access can be restricted | Measure 1.1.2: free-form text > 200 tokens must be watermarked; 2.1.2 restricted detector access ✅ | HF SynthID on SmolLM2-360M: **12/12** at 80-150 tokens; drop 30% words 10/12; typos 8/12; LLM paraphrase **1/6**; translation cycle 6/6 (41% 4-gram overlap); **false alarms 5/24 at 20 tokens** |
| **Fingerprinting / perceptual hash + registry** | Finds unmarked copies of content the provider generated (lookup) | Geometric edits; needs a registry of every output; privacy and storage cost; hash collisions between similar images | No standard registry; C2PA soft binding can use it as a locator ✅ spec | Measure 1.1.3: optional, "not sufficient" alone; logging limited to output data, privacy-preserving ✅ | dHash 256 bits: survived JPEG/resize/noise/1:1 screenshot; **0/3** after crop, rotate, mirror, 125% screenshot; unrelated images >= 105 bits apart |
| **Logging** (provider keeps outputs/IDs) | Authoritative "did we make this" for a given output | Needs the content or a hash; retention + privacy burden; outsiders cannot check | none | with fingerprinting, optional, "not sufficient" ✅ | not tested |
| **Forensic classifiers** (AI-vs-human detectors) | Work without any marking, on any content | Poor out-of-domain, higher false positives for some groups (e.g. non-native English writers) ✅ (Nature paper, citing Liang et al.); arms race | none | 2.2 forensic detection: optional ✅ | our null set: human 19th-century prose and LLM text both stayed under the watermark threshold; we did not test a classifier |
| **Visible label / "AI" icon** (deployer side) | Human-perceivable disclosure (Art. 50(4)) | Cropped or re-uploaded without the label; text label separated from text | EU icon with capital "AI" ✅ Code Section 2 | Section 2, repeated in video ✅ | n/a |

## 2. Combination, as the Code envisions it (our reading)

```
generate -> watermark (layer 2, survives re-encode)  -> sign C2PA manifest (layer 1, rich + tamper-evident)
         -> [optional] fingerprint/log (layer 3, lookup of what we made)
verify   -> manifest present? validate + trust ->  else watermark detect -> else fingerprint lookup -> else "unknown"
```
Lab evidence (ex2): which layer answers depends on what happened to the file. Intact -> C2PA; re-compressed/resized/noisy ->
watermark and/or fingerprint; crop/rotate/mirror/scaled screenshot -> none of our three layers (4/11) 🧪.
Policy implication: "marking present" is evidence; "marking absent" is **not** evidence of human origin.

## 3. Decision guide (engineering, not legal)

| Situation | Reasonable stack | Why |
|---|---|---|
| Chatbot/agent (Art. 50(1)) | system-owned first-turn notice + persistent badge; deterministic answer to "are you human?"; for agents say "AI **and** on whose behalf" | prompt-only fails (0/10 informed; 15/20 human claims under persona) 🧪; Guidelines 31, 35-38 ✅ |
| Image/video generator you operate | signed C2PA + learned invisible watermark; detector API; optional fingerprint registry | Code 1.1; each layer fails differently 🧪 |
| Text generator | watermark only above ~200 tokens; metadata where the channel allows; restricted detector; do **not** sell a classifier verdict as proof | Code 1.1.2/2.1.2 ✅; our false alarms and paraphrase result 🧪 |
| Legacy generative system placed on the market before 2 Aug 2026 | marking can wait to 2 Dec 2026; chatbot disclosure and deployer duties cannot | Art. 111(4) ✅; Guidelines 153-154 ✅ |
| You only deploy someone else's generator (deepfake / public-interest text) | label with the "AI" icon; keep editorial-control records if you rely on the text exception | Art. 50(4) ✅, Code Section 2 ✅ |
| You need to *check* content | check manifest -> watermark detectors of known vendors -> treat the rest as unknown | detection interoperability still maturing (3.4(c), 2 Feb 2027) ✅🔮 |

Caveats: images are 3 procedural samples and every layer is an open stand-in; no claim is made about SynthID, TrustMark, Video Seal or any
vendor's measured robustness. See `research.md` section 5.
