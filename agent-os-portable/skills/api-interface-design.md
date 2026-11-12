# API and interface design skill
1. Define the caller, provider, trust boundary, data ownership and failure semantics.
2. Specify typed request/response schemas, validation, error codes, timeouts, retries and idempotency.
3. Prefer backward-compatible additive changes; version breaking contracts explicitly.
4. Keep credentials server-side and apply least-privilege scopes to tools and service accounts.
5. Define contract tests and examples for success, validation failure, timeout and partial failure.
6. Document rate limits, observability, pagination and deprecation behavior.
