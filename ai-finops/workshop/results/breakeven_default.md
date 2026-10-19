Replica: 8 GPUs x $3.5/h = $20,440/month always-on, + ops $15,000 = $35,440/month fixed
Capacity at 100% utilization: 6.57B output tokens/month (+10x input tokens each)

| API | API $ per 1M output tok (incl. its input) | self-host break-even volume | break-even utilization |
|---|---|---|---|
| open-weights via API (0.60/2.40) | $8.40 | 4.22B out tok/month | 64% |
| frontier API (2.00/10.00) | $30.00 | 1.18B out tok/month | 18% |

Self-hosted $ per 1M output tokens (incl. input) by utilization:
| utilization | 5% | 10% | 25% | 50% | 75% | 100% |
|---|---|---|---|---|---|---|
| self-host | $107.88 | $53.94 | $21.58 | $10.79 | $7.19 | $5.39 |

Read it as: below the break-even utilization the API is cheaper. Arithmetic check: traffic only in business hours (50 of 168 h/week) caps an always-on replica at ~30% average utilization even if it is saturated during those hours. The frontier row compares different models (quality differs) - it answers 'what if a self-hosted open model is good enough for this task', which your evals must confirm.
