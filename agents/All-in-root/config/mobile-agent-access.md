# Mobile access: Conduit and Lody

This guide uses the existing VPS and agent fleet; it does not create a second agent.

## Private network prerequisite
- Connect the phone/desktop to the owner's Tailscale network first.
- Do not expose LiteLLM, Qdrant, Docker API, agent control APIs, or dashboards directly to the public Internet.
- The LiteLLM gateway remains bound to `127.0.0.1:4000`; use OpenWebUI as the mobile-friendly frontend unless an authenticated private reverse proxy has been explicitly configured.

## Conduit (OpenWebUI client)
1. Connect the phone to Tailscale.
2. In Conduit, add the existing OpenWebUI server using the Tailscale URL `http://100.126.48.60:8081`.
3. Sign in with the existing OpenWebUI account. Do not put the LiteLLM master key into an unauthenticated public URL.
4. Verify that existing provider connections are still present before selecting a model. The current VPS inventory previously found 14 provider connections; this guide does not modify them.

If Conduit requires an OpenAI-compatible endpoint rather than an OpenWebUI server, do not point it at the loopback-only gateway from the phone. First provision an authenticated HTTPS/Tailscale-only reverse proxy and a least-privilege client key.

## Lody / OpenHands
- OpenHands UI: `http://100.126.48.60:3000` while connected to Tailscale.
- Lody is a tool/runtime surface, not a separate agent to duplicate. Keep the current runtime identity and its credentials; do not create a second daemon for the same role.
- If the client reports an API error, test authentication and model inference separately. A model catalog response does not prove that generation works.

## Troubleshooting
- Confirm Tailscale connectivity and that the target address is the VPS's current Tailscale IP.
- Check `systemctl is-active agent-docker-port-guard.service`.
- Check `bash deploy/verify-current-vps.sh` from the All-in checkout.
- Do not open ports 3000, 3001, 33601, 4000, 4001, 6333, or 6334 to the public Internet to fix a mobile connectivity issue.
