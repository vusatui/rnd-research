Replica: 8 GPUs x $10.0/h = $58,400/month always-on, + ops $15,000 = $73,400/month fixed
Capacity at 100% utilization: 6.57B output tokens/month (+10x input tokens each)

| API | API $ per 1M output tok (incl. its input) | self-host break-even volume | break-even utilization |
|---|---|---|---|
| open-weights via API (0.60/2.40) | $8.40 | 8.74B out tok/month | 133% (impossible: >100%) |
| frontier API (2.00/10.00) | $30.00 | 2.45B out tok/month | 37% |

Self-hosted $ per 1M output tokens (incl. input) by utilization:
| utilization | 5% | 10% | 25% | 50% | 75% | 100% |
|---|---|---|---|---|---|---|
| self-host | $223.44 | $111.72 | $44.69 | $22.34 | $14.90 | $11.17 |

Read it as: below the break-even utilization the API is cheaper. Arithmetic check: traffic only in business hours (50 of 168 h/week) caps an always-on replica at ~30% average utilization even if it is saturated during those hours. The frontier row compares different models (quality differs) - it answers 'what if a self-hosted open model is good enough for this task', which your evals must confirm.
