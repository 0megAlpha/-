# VPS port and exposure policy

The full current listener inventory belongs in the private VPS maintenance record, not this public repository.

- Keep administrative dashboards, agent APIs, model gateways, vector databases, Redis, Docker APIs and MCP control planes on loopback or the private overlay.
- Do not treat a Docker 0.0.0.0 bind as safe merely because a private-network URL is used by a client.
- Require authentication and least-privilege credentials for every remote API.
- Do not expose model gateways or vector databases directly to mobile clients. Use a verified authenticated private reverse proxy.
- Before changing exposure, record the current listener, firewall, Docker published-port and Tailscale state; test from both a private client and an external network.
- Do not rely on historical port-guard service names or old deployment reports. Re-query the current systemd unit and firewall state.
- Never store API keys in browser localStorage or commit populated environment files.

No current listener inventory or private Tailscale addresses are published in this file.
