# Private mobile access

This guide is intentionally endpoint-agnostic. Configure the current private Tailscale hostname/IP and service URLs in a local, ignored environment file; do not commit private addresses or tokens.

1. Connect the phone to the owner's Tailscale network.
2. Use the configured private OpenHands and Open WebUI URLs.
3. Do not connect a mobile client directly to LiteLLM, Qdrant, Redis, Docker API, or MCP administration endpoints.
4. Hermes is loopback-bound on the current VPS. Mobile access requires an authenticated private reverse proxy; do not change its bind address merely to make a client connect.
5. Do not use port 8081 as an Agent dashboard proxy unless its service implementation has been reviewed and replaced with a dedicated authenticated proxy.
6. API keys must be entered into the client session or a secure credential store. Never persist them in localStorage or a URL.
7. Verify model inference separately from model catalog visibility and agent tool execution.

The All-in dashboard's optional Hermes/Qdrant proxy routes must be implemented and authenticated before they are configured as defaults.
