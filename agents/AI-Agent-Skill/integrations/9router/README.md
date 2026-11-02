# 9Router Fleet Integration

## Runtime
- Package: 9router 0.5.95
- Bind: 127.0.0.1:20128 only
- API: http://127.0.0.1:20128/v1
- State: /root/.9router/db/data.sqlite
- Service: 9router.service

## Security boundary
9Router is loopback-only. It is not exposed on the VPS public interface.
Provider credentials are stored by 9Router's provider-connection database and are not committed to Git.
Production request-body logging remains disabled.

## GPT-OSS 120B
- Native Groq model: openai/gpt-oss-120b
- 9Router catalog ID: groq/openai/gpt-oss-120b
- Provider: Groq
- Required credential: Groq API key, configured through 9Router's provider dashboard/connection store.
- The model is present in the local 9Router catalog.
- Inference is not considered provisioned until a valid Groq credential is connected and a live completion test succeeds.

## Fleet contract
Clients should use the loopback OpenAI-compatible endpoint through the fleet integration layer rather than calling providers directly.
Recommended model alias: groq/openai/gpt-oss-120b.

## Verification
Run:
  systemctl is-active 9router.service
  ss -lntp | grep ':20128'
  curl -sS http://127.0.0.1:20128/v1/models

A 401 on /v1/chat/completions without an API key is expected when 9Router API-key enforcement is enabled.
