# Canonical OpenHands Deployment

This is the single intended OpenHands runtime for this VPS. It uses the official OpenHands Agent Canvas all-in-one image, pinned to upstream version 1.27.1 with the Browser MCP compatibility patch maintained in the private AI-AGENT-SKILL repository.

## Security contract

- The container backend binds to 127.0.0.1:8009 only.
- Nginx is the only entry point and must bind to the Tailscale address.
- AGENT_CANVAS_ALLOW_LAN_SESSION_KEY is enabled only because the published host port is loopback-only and the reverse proxy is Tailscale-only. Never change the port mapping to 0.0.0.0.
- No API keys or provider credentials belong in this repository. Runtime model credentials live in the OpenHands state profile or secret store.
- The Docker socket is mounted because the OpenHands agent needs to create isolated runtime containers. Treat access to this service as privileged.

## Build and validate

From this directory:

    docker compose -f compose.yaml build --pull
    docker compose -f compose.yaml config --quiet
    docker compose -f compose.yaml up -d
    docker compose -f compose.yaml ps

The final cutover must also verify /health, /ready, /canvas/, session-authenticated API access, a real model response, MCP tool discovery, and Browser MCP clean shutdown before retiring old containers.
