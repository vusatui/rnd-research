similarity (bge-small-en-v1.5 embeddings): paraphrases mean 0.824 [min 0.676, max 0.919] | near-misses mean 0.836 [min 0.680, max 0.946]
exact-match cache: 0/12 paraphrase hits, 0/12 false hits

| threshold | paraphrase hits (saved calls) | near-miss hits (WRONG answers served) |
|---|---|---|
| 0.70 | 11/12 | 10/12 |
| 0.75 | 11/12 | 9/12 |
| 0.80 | 8/12 | 9/12 |
| 0.85 | 3/12 | 6/12 |
| 0.90 | 2/12 | 4/12 |
| 0.95 | 0/12 | 0/12 |

Worst near-misses (highest similarity, different answer):
  0.946  'Is SAML SSO available on the Business plan?'  vs  'Is SAML SSO available on the Enterprise plan?'
  0.932  'How do I export all my invoices?'  vs  'How do I import all my invoices?'
  0.923  'What is the refund window for annual plans?'  vs  'What is the refund window for monthly plans?'
  0.914  'What is the API rate limit on the Team plan?'  vs  'What is the API rate limit on the Business plan?'
