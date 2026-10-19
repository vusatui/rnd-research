# AI cost control (FinOps for AI, token cost engineering)

Research topic #3 ([issue](https://github.com/vusatui/rnd-research/issues/3)). The ask this prepares for: *"Our LLM
bill exploded - show us who spends it, on what, and cut it without breaking quality."*

| File | What |
|---|---|
| [`research.md`](research.md) | Fact-checked notes (2026-10-19): why bills surprise, FinOps Foundation guidance, FOCUS 1.4/1.5, unit economics, levers (routing, caching, semantic caching, batch, compression, distillation, self-hosting), attribution and budgets, pricing trends, consensus vs disputed, open items |
| [`comparison.md`](comparison.md) | Gateways (LiteLLM, Portkey/Prisma AIRS, Cloudflare, OpenRouter, Azure APIM, Bedrock, Kong, Envoy), observability, provider price levers, lever decision table - with prices and dates |
| [`talk-outline.md`](talk-outline.md) | ~35-minute talk outline with timing |
| [`workshop-plan.md`](workshop-plan.md) | ~2.5-3 h workshop agenda and the measured results |
| [`workshop/`](workshop/) | Runnable code: lever lab, prompt-cache probe and simulator, semantic-cache stress test, LiteLLM gateway with team budgets, FOCUS-shaped chargeback, self-host break-even |

Key measured results (free OpenRouter models, shadow-priced at published paid prices, n=16 tickets, 2026-10-19):
concise output -26% cost with equal-or-better quality; context trimming -68%; small model -96% at the same pass
rate; stacking small model + trimming -98% but 9/16 pass; a cascade needed a deterministic grounding check to catch a
hallucinated price; LiteLLM blocked a team at 112% of its budget.
