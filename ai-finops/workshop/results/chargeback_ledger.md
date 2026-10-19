347 FOCUS-shaped rows from 169 calls -> /workspace/rnd-research/ai-finops/workshop/out/focus_cost_usage.csv

Chargeback (shadow ListCost, paid-twin prices):
| team | config | model | direction | cache | tokens | ListCost $ |
|---|---|---|---|---|---|---|
| support | A_baseline | nemotron-3-ultra-550b-a55b | Input | Uncached | 76,170 | 0.045702 |
| support | A_baseline | nemotron-3-ultra-550b-a55b | Output | Uncached | 7,287 | 0.017489 |
| support | B_concise | nemotron-3-ultra-550b-a55b | Input | Uncached | 67,455 | 0.040473 |
| support | B_concise | nemotron-3-ultra-550b-a55b | Output | Uncached | 1,361 | 0.003266 |
| support | C_stable | nemotron-3-ultra-550b-a55b | Input | Uncached | 67,487 | 0.040492 |
| support | C_stable | nemotron-3-ultra-550b-a55b | Output | Uncached | 1,400 | 0.003360 |
| support | D_trim | nemotron-3-ultra-550b-a55b | Input | Uncached | 27,442 | 0.016465 |
| support | D_trim | nemotron-3-ultra-550b-a55b | Output | Uncached | 1,574 | 0.003778 |
| support | E_small_dyn | nemotron-3.5-lightning | Input | Uncached | 67,470 | 0.004723 |
| support | E_small_dyn | nemotron-3.5-lightning | Output | Uncached | 1,262 | 0.000252 |
| support | F_small_full | nemotron-3.5-lightning | Input | Read | 12,576 | 0.000503 |
| support | F_small_full | nemotron-3.5-lightning | Input | Uncached | 194,058 | 0.013584 |
| support | F_small_full | nemotron-3.5-lightning | Output | Uncached | 3,986 | 0.000797 |
| support | G_small_trim | nemotron-3.5-lightning | Input | Uncached | 24,585 | 0.001721 |
| support | G_small_trim | nemotron-3.5-lightning | Output | Uncached | 1,304 | 0.000261 |
| support | probe_dynamic | nemotron-3.5-lightning | Input | Uncached | 25,300 | 0.001771 |
| support | probe_dynamic | nemotron-3.5-lightning | Output | Uncached | 525 | 0.000105 |
| support | probe_dynamic_pad1 | nemotron-3.5-lightning | Input | Uncached | 32,561 | 0.002279 |
| support | probe_dynamic_pad1 | nemotron-3.5-lightning | Output | Uncached | 383 | 0.000077 |
| support | probe_stable | nemotron-3.5-lightning | Input | Uncached | 25,303 | 0.001771 |
| support | probe_stable | nemotron-3.5-lightning | Output | Uncached | 505 | 0.000101 |
| support | probe_stable_pad1 | nemotron-3.5-lightning | Input | Read | 18,864 | 0.000755 |
| support | probe_stable_pad1 | nemotron-3.5-lightning | Input | Uncached | 13,692 | 0.000958 |
| support | probe_stable_pad1 | nemotron-3.5-lightning | Output | Uncached | 376 | 0.000075 |
