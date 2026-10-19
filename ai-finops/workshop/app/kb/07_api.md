# [api] Public API and webhooks

The REST API is available on Team, Business and Enterprise. Authentication uses API keys created under Settings > Developers; keys are shown once and can be scoped read-only or read-write.

Rate limits: standard (Team) 60 requests per minute and 10,000 per day; elevated (Business) 300 requests per minute and 100,000 per day; Enterprise is negotiated. Exceeding the limit returns HTTP 429 with a Retry-After header. Limits apply per workspace, not per key.

Pagination is cursor-based with a maximum page size of 100 items.

Webhooks: events invoice.created, invoice.sent, invoice.paid, invoice.overdue, payment.failed, customer.created. Payloads are signed with HMAC-SHA256 in the Ledgerly-Signature header. Failed deliveries are retried with exponential backoff for up to 24 hours (8 attempts), then the endpoint is disabled and the owner is emailed.

Sandbox: every workspace on Team and above can create one sandbox workspace with fake data; sandbox API calls do not count toward rate limits.

API versioning: date-based versions (for example 2026-04-01) pinned per key. Deprecated versions are supported for at least 12 months after the deprecation notice.

There is no GraphQL API. There are official SDKs for Python and JavaScript/TypeScript only.
