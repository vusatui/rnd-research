# R&D Research

A collection of R&D research. Each topic lives in its own folder and includes an overview, comparisons, talk/presentation materials and, where relevant, a workshop with ready-to-run code.

## Topics

| Folder | Topic | Status |
|---|---|---|
| [`sandboxes-and-remote-desktops/`](./sandboxes-and-remote-desktops/) | Sandboxes and remote desktops for AI agents: why they matter, threat model, isolation technologies, platform comparison (E2B, Daytona, Modal, etc.), talk and workshop | Draft |
| [`system-one-models/`](./system-one-models/) | System One / decision models: TypeSafe Jev, OpenAI Decisions API, Cloudflare Clef, Unsloth recipe; System 1 vs System 2, classifiers, rerankers, routers, guardrails; talk and workshop | Draft |

## Rules

- One topic = one top-level folder with its own `README.md`.
- Never commit secrets: use `.env` (it is in `.gitignore`) with `.env.example` as a template.
