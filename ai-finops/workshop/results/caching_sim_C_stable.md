C_stable: avg input 4,218 tok = stable prefix ~4,173 + per-ticket ~45

Input-token cost multiplier vs no caching, by requests sharing the prefix within one TTL window:
| provider rule | N=1 | N=2 | N=5 | N=20 | N=100 |
|---|---|---|---|---|---|
| no caching | 1.00x | 1.00x | 1.00x | 1.00x | 1.00x |
| OpenAI GPT-5.6+ (0.10x) | 1.25x | 0.68x | 0.34x | 0.17x | 0.12x |
| OpenAI gpt-6.1-sol (0.05x) | 1.25x | 0.65x | 0.30x | 0.12x | 0.07x |
| Anthropic 5-min (0.10x) | 1.25x | 0.68x | 0.34x | 0.17x | 0.12x |
| Anthropic 1-hour (0.10x) | 1.99x | 1.05x | 0.49x | 0.20x | 0.13x |
| Gemini implicit (0.05x) | 1.00x | 0.53x | 0.25x | 0.11x | 0.07x |

N=1 means a cache write that is never read: caching with a write premium then costs MORE than no caching. A dynamic value at the top of the prompt (config A/B/E: timestamp + ticket id) makes every request N=1.
Measured on the free endpoint in this run: cache hit rate 0% of input tokens.
