# Exercise 3: fast first, priced

**Problem.** A threshold trades errors against human work. Which threshold is cheapest?

**Design.** System 1 = a method from Exercise 2 (default Jev). Gate: automate when p(answer) ≥ threshold. System 2 = a human queue (always right, `--review` $ per ticket) or another ex2 method (`--s2`). Every wrong automated answer costs `--error-cost`.

**Run.** `make ex3` or `make ex3 S1=verbal_deepseek-v4.1-flash-1017 ERROR_COST=20 REVIEW=1`. No key needed (uses `results/`).

**Result** (error $5, review $0.50, per 1,000 tickets): Jev at threshold 0.95 automates 75% with 0 errors on the test set, $127 total, against $333 with no gate and $500 with humans only. Verbalized deepseek reaches the same $127 at 0.85; the knob just has fewer positions.
