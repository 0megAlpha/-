# Mobile clients: Lody and Conduit

This host already runs Lody CLI 0.103.0 and an enabled lody-agent.service. The service process is active, but the CLI reports Not logged in; a Lody device-authorization flow must be completed before the machine appears in the Lody mobile workspace.

## Lody iOS

1. Install the official Lody app from the App Store.
2. Sign in to the same Lody account used for the CLI device authorization.
3. Complete the one-time device authorization shown by lody login --machine-name agent-vps.
4. After login, verify the machine with lody machine list; add /home/xiaye/agent-os-portable using lody project add /home/xiaye/agent-os-portable.
5. Add the other project roots individually only after their repository boundaries and permissions have been checked.

Official docs: https://lody.ai/docs/quickstart/ and https://lody.ai/docs/mobile/

## Conduit iOS

Conduit supports Open WebUI, OpenAI-compatible APIs, Ollama, OpenRouter and a Hermes agent backend. The VPS already runs Open WebUI 0.13.3 and its /health endpoint returns {"status":true} on the existing host port 3000.

Recommended initial connection:
- Backend: Open WebUI
- Server URL: http://<TAILSCALE_IP>:3000
- Network: the iPhone must be connected to the same Tailscale network.
- Sign-in: use the existing Open WebUI account; do not place passwords or API keys in this repository.

The current host Tailscale IPv4 address is deliberately not stored in this public repository. Obtain it on the VPS with tailscale ip -4. No port was added for this setup; it uses the already-published Open WebUI port 3000.

Hermes API currently listens on loopback 127.0.0.1:8642, so it is not directly reachable from the iPhone. Do not expose it by opening a port. Keep Open WebUI as the initial Conduit backend until a supported private proxy path is verified.

Official site: https://conduit.mobile/
iOS App Store: https://apps.apple.com/tw/app/conduit-ai-coding-remote/id6775726887
