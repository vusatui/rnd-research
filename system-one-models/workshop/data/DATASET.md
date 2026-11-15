# Dataset: 250 synthetic support tickets for "Lumen" (a made-up B2B analytics SaaS)

`tickets.jsonl`, one ticket per line. Built by `make_dataset.py` on 2026-11-15; every raw model output is in `raw/`, the call log with tokens and $ is in `generation_log.json`.

| | |
|---|---|
| Tickets | 250: **100 train** (only the classic classifier learns from them), **150 test** (every method is scored on these) |
| Questions | `department` (billing, technical, account, sales, other) and `urgency` (low, medium, high) |
| Generator | `baidu/ernie-5.5-flash-preview:free`: 10 batches x 25, each batch a different writing persona (terse admin, upset owner, non-native speaker, developer with error codes, procurement, phone typing, analyst mixing topics, confused trial user, agency, CTO), fixed quota of 5 tickets per department, an urgency mix and 6-7 deliberately borderline tickets |
| Labellers (blind) | `particle-ai/particle-1:free` and `openai/gpt-6-luna`; they never see the intended label |
| Gold label | majority of (generator intent, labeller 1, labeller 2) |
| Agreement | labellers agree on department 97.6%, on urgency 90.0%; gold equals the generator's intent for 93.6% of departments |
| `ambiguous` | the two blind labellers disagree on department: 6 tickets (4 in test) |
| Length | 16 to 94 words, median 49 |
| Cost | $0.006 (the generator and one labeller are free models) |

Fields: `id, split, text, department, urgency, ambiguous, generator_borderline, also_plausible, intent{department,urgency}, labels{model: {department, urgency}}, persona`.

## Caveats (say them out loud in the workshop)

- **Synthetic and LLM-labelled.** Gold labels are an LLM consensus, so methods that think like an LLM have a home advantage. A real ticket log with human labels is the honest next step; the harness takes any JSONL with the same fields.
- **Department is easy, urgency is not.** Department is close to topic classification (strong methods reach 93-97%); urgency is subjective (labellers agree only 90%), and that is where calibration differences show.
- **150 test tickets** is enough to see big differences, not small ones: one ticket is 0.7 percentage points.
