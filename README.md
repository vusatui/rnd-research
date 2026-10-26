# R&D Research

A collection of R&D research. Each topic lives in its own folder and includes an overview, comparisons, talk/presentation materials and, where relevant, a workshop with ready-to-run code.

## Topics

| Folder | Topic | Status |
|---|---|---|
| [`sandboxes-and-remote-desktops/`](./sandboxes-and-remote-desktops/) | Sandboxes and remote desktops for AI agents: why they matter, threat model, isolation technologies, platform comparison (E2B, Daytona, Modal, etc.), talk script, HTML slides and workshop; plus a light 30-min version for a general audience in `presentation/` (Excalidraw) | Draft |
| [`system-one-models/`](./system-one-models/) | System One / decision models: TypeSafe Jev, OpenAI Decisions API, Cloudflare Clef, Unsloth recipe; System 1 vs System 2, classifiers, rerankers, routers, guardrails; talk script, HTML slides and workshop; plus a light 30-min version for a general audience in `presentation/` (Excalidraw) | Draft |
| [`legacy-modernization/`](./legacy-modernization/) | AI-assisted legacy modernization (COBOL, mainframe, old Java/.NET): client demand, AWS Transform / IBM Bob for Z / Google MAT + Dual Run / Microsoft / Mechanical Orchard / deterministic converters, why verification (the "diamond") is the product; workshop on AWS CardDemo with GnuCOBOL + free LLMs | Done |
| [`agents-pilot-to-prod/`](./agents-pilot-to-prod/) | AI agents from pilot to production: why pilots stall, governance by autonomy level, OpenTelemetry GenAI tracing, evals with a regression gate, LLM-as-judge pitfalls, guardrails at the tool boundary, cost/latency budgets, EU AI Act hooks; tool comparison (Langfuse, Phoenix, LangSmith, Braintrust, Promptfoo, Inspect, NeMo Guardrails, AgentCore...); workshop with tracing, evals, red team and budgets on free models | Done |
| [`ai-finops/`](./ai-finops/) | AI cost control (FinOps for AI, token cost engineering): why AI bills surprise, FinOps Foundation guidance, FOCUS 1.4/1.5 for AI, $ per successful task, levers (output control, context trimming, routing/cascades, prompt and semantic caching, batch, distillation, self-host break-even), attribution and budgets via gateways; comparison (LiteLLM, Portkey/Prisma AIRS, Cloudflare, OpenRouter, Azure APIM, Bedrock, Kong, Envoy, Langfuse); workshop with a lever lab, cache probe, LiteLLM team budgets and FOCUS-shaped chargeback on free models; talk script, HTML slides and participant guide | Done |
| [`ai-act-art50-transparency/`](./ai-act-art50-transparency/) | EU AI Act Article 50 (transparency): telling people they talk to AI, marking AI-generated content, provider vs deployer duties, the Digital Omnibus changes and dates, Code of Practice and Guidelines; comparison of C2PA content credentials, watermarks, metadata and fingerprints; workshop with chatbot disclosure red-team, C2PA signing and survival test, text watermark attacks on free models; talk script, Excalidraw deck and participant guide. General information, not legal advice | Done |

## Rules

- One topic = one top-level folder with its own `README.md`.
- Never commit secrets: use `.env` (it is in `.gitignore`) with `.env.example` as a template.

## Backlog

The single source of truth for topics and their status is the [R&D Research project board](https://github.com/users/vusatui/projects/3).
