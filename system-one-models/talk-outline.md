# Talk outline: "System One models - when AI should decide, not write" (~35 min)

1. **Hook (3 min).** The same ticket routed by a reasoning LLM (3 s, a paragraph of text to parse) vs a decision model (one probability, < 0.5 s). Question: why are we generating prose to make a yes/no decision?
2. **System 1 vs System 2 (4 min).** Kahneman; mapping to software: LLM = slow verbal reasoning; most production AI calls are actually snap judgments (classify, route, gate, rank). AlphaGo analogy: policy network (intuition) + search (deliberation).
3. **The news (5 min).** Sept-Oct 2026: TypeSafe Jev, OpenAI Decisions API (beta), Cloudflare Clef (open weights), Unsloth recipe to train your own (the LinkedIn post), Laya / Liquid d1. Clearly label what is verified vs vendor claims.
4. **Anatomy of a decision model (6 min).** State + typed questions → probabilities. Primitives: yes-probability (noul/predicate), choice, score. Under the hood: read once, scoring head over options, no decoding; output tokens free. Probability vs confidence; calibration and ECE in one slide.
5. **It is not new - generalization (5 min).** Classifiers, rerankers, reward models, embeddings, routers, guardrails all are "System 1". What is new: zero-shot, instruction-following, general, with a standard (Jev-compatible) API. Comparison table.
6. **Architecture patterns (5 min).** Confidence-gated cascade (S1 → S2 → human), speculative fan-out (many questions in one call), composite scoring in code, guardrails in/out of an LLM, agent tool/skill selection.
7. **Live demo (4 min).** Workshop ex1 + ex3: classifier vs LLM-as-decider, threshold sweep.
8. **Pitfalls & checklist (2 min).** Pin model versions (thresholds shift), calibrate on your own labels, confidence formulas differ across vendors, English-first, vendor benchmarks, data residency.
9. **Q&A (1 min+).**
