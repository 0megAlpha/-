# Devin Service Adapter

Devin is a hosted coding-agent service. Its public API and MCP integrations manage sessions, tasks, repositories, and workspaces. This is a service-control adapter, not a claim that Devin supports arbitrary custom inference base URLs.

- `DEVIN_API_BASE_URL`: official service API root for the account/product API version.
- `DEVIN_API_KEY`: Devin service credential, injected at runtime.
- Connect the target GitHub repository inside Devin's own Integrations/Teams settings.
- Use the Devin API/MCP adapter for task/session operations; use separate supported model-provider settings only if Devin documents them for the account.

See `devin.env.example`. Live service API verification requires a valid Devin credential.
