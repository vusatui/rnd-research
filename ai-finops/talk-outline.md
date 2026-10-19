# Talk outline (~35 min): "Tokens got cheaper. Why did your AI bill go up?"

Audience: engineers, architects, delivery leads and pre-sales working with enterprise clients. Goal: explain why AI
spend surprises organizations, how to make it visible and attributable, and which engineering levers cut it -
with their quality risks - using numbers from a live workshop run.
Legend: ✅ verified source, 🟡 vendor/survey claim, 🔮 forecast, 🧪 measured in our workshop (see `research.md`,
`workshop-plan.md`). This is an outline only (no script, no slides).

| # | Min | Section | Content | Visual / demo |
|---|---|---|---|---|
| 1 | 0-3 | Hook | Same 16 support tickets, same quality: $1,250/month vs $46/month at 100k tickets 🧪. And one config that is 98% cheaper but answers 7 of 16 wrong 🧪. Question: which number does your CFO see, and which does your customer see? | Two-column $/month vs pass-rate |
| 2 | 3-7 | Why bills surprise | Unit price falls ~13x/yr for fixed capability (Epoch) ✅, but Gartner: cost per agentic workflow 5x+ through 2028 🔮; Accenture: 9 in 10 execs spend savings on more use cases 🟡; McKinsey interviews: pilot→prod ~4x, bad agents up to 30x tokens 🟡. Mechanisms: re-sent context, output 5x input price, reasoning billed as output, long-context and speed multipliers, promos ending (Gemini 4 Argon doubles 1 Dec 2026) ✅ | "Price per token ↓ / tokens per task ↑" chart |
| 3 | 7-11 | FinOps for AI: the community playbook | State of FinOps 2026: 98% manage AI spend ✅. FinOps Foundation: Price x Quantity, showback → chargeback, quotas, anomaly detection, KPIs (cost per inference/token/call, model-choice quality) ✅. FOCUS 1.4 today; 1.5 draft adds ModelId, token direction/cache action, PrincipalId (ratification planned 3 Dec 2026) ✅ | FOCUS 1.5 columns on one slide |
| 4 | 11-14 | The unit metric | $/task, $/successful task, $/month at forecast volume; shadow-price free/internal models; state the price card and date. Twin vs frontier card changes the large/small gap from ~9x to ~20x 🧪 | Workshop summary table |
| 5 | 14-22 | Levers with numbers | Lever lab 🧪: concise output -26% (quality up), context trimming -68%, small model -96%, small+trim -98% but 9/16. Research ranges: RouteLLM >2x, FrugalGPT up to 98% on one dataset, LLMLingua 20x, batch -50% ✅. Rule: levers interact - re-run evals after each | Live: `run_levers.py --rescore`; bar chart cost vs pass |
| 6 | 22-25 | Cascades need a real validator | Small model invented "$9,900/yr" for Enterprise with high self-reported confidence; a 10-line grounding check caught it and escalated 🧪 | Side-by-side replies T11 |
| 7 | 25-28 | Caching: free money and traps | Provider rules: write 1.25x / read 0.1x (OpenAI, Anthropic), Gemini implicit ✅; dynamic header first = 0 cached tokens, stable = 6,288/request 🧪; written-once cache costs 1.25x 🧪. Semantic cache: near-misses score above paraphrases, 9/12 wrong answers at 0.80 🧪; vCache ✅ | Cache-probe output; similarity histogram |
| 8 | 28-31 | Attribution and budgets | One path via a gateway; AWS guidance: stamp tags in the gateway, low-cardinality tags, reconcile with invoice ✅. Live LiteLLM: team blocked at 112% of budget, allow-list 403, $0-pricing gotcha 🧪. Cloudflare/Azure/Kong equivalents ✅ | Live gateway run + chargeback table |
| 9 | 31-33 | Self-host or API? | Break-even is a utilization question: 64% vs open-model API, 18% vs frontier price on stated assumptions 🧪; GPU price spread $3.5 vs ~$10/h 🟠; business hours cap at ~30% | Utilization curve |
| 10 | 33-35 | Checklist + Q&A | 1) unit metric + eval set, 2) shadow prices, 3) gateway as the only path, attribution tags, 4) budgets with headroom + anomaly alerts, 5) levers by risk: output → caching → trimming → batch → routing with deterministic validator → semantic cache last, 6) FOCUS-shaped export for finance | One-slide checklist |

Backup material: provider price-lever table (`comparison.md` §4); caching simulator table; FOCUS-shaped CSV sample;
gateway comparison; "numbers not to quote without context" (McKinsey 30x, FrugalGPT 98%, semantic-cache stress test).
