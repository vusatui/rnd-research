# EU AI Act Art. 50: transparency for AI-generated content and AI interaction

What Art. 50 actually requires from 2 August 2026 (chatbot disclosure, machine-readable marking and detection of generated
content, deepfake and public-interest-text labels), what the Digital Omnibus changed (very little for Art. 50), what the
Commission's Guidelines and the Code of Practice add, and how the marking techniques - C2PA, signed metadata, invisible
watermarks, fingerprinting/logging, classifiers - compare, with a runnable workshop that measures where each one breaks.

> **General information, not legal advice.** Engineering-oriented reading of public sources as of 2026-10-26.

- [`research.md`](research.md) - sources (checked 2026-10-26) with ✅/🟡/🟠/❌/🧪/🔮 markers: Art. 50 text, Omnibus
  Regulation (EU) 2026/1744 (read on EUR-Lex), Commission Guidelines C(2026) 5054, Code of Practice on Transparency of
  AI-generated Content, technique facts, our measurements, consensus vs disputed, open items
- [`comparison.md`](comparison.md) - C2PA, unsigned metadata, invisible watermarks (DWT-DCT-SVD, SynthID, TrustMark,
  Video Seal, Tree-Ring), text watermarking, fingerprinting/logging, forensic classifiers, visible labels: what each
  gives, how it is stripped, interoperability, where it sits in the Code; decision guide
- [`talk-outline.md`](talk-outline.md) - ~35 min talk, 9 segments with timing
- [`workshop-plan.md`](workshop-plan.md) + [`workshop/`](workshop/) - 3 exercises (chatbot disclosure red-team,
  C2PA + watermark + fingerprint survival, text watermark) with real measured results; free OpenRouter models only,
  everything else runs offline on CPU

Quick start:

```bash
cd workshop
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python -m pytest -q tests                  # offline, no key
python ex2_c2pa/survival.py                # C2PA / watermark / fingerprint survival table, offline
cp .env.example .env                       # add a free OpenRouter key for ex1
python ex1_disclosure/run_redteam.py       # 60 free-model requests
```

Status: Stage 1 done (2026-10-26): research, comparison, talk outline, workshop, workshop plan. Talk script and slides: not started.
