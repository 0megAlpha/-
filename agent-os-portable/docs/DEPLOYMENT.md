# Deployment and integration runbook

## Current integration targets

- OpenHands: existing service; preserve its current container, volumes and runtime.
- LiteLLM: existing OpenAI-compatible gateway; use configured model aliases only.
- Dify: existing workflow installation; use its authenticated API only after checking the installed version's route/schema.
- Open WebUI: existing user interface; keep its existing model connection.
- GitHub: authenticated connector account 0megAlpha; do not restore former account credentials.

## Safe activation

1. Install this package into its isolated Python 3.12 environment.
2. Populate .env with local credentials; never paste credentials into chat or commit them.
3. Confirm the LiteLLM endpoint and model alias with a local health/model-list request.
4. Run unit tests and a dry-run planning request.
5. Configure OpenHands workspace mapping only after selecting the intended repository directory.
6. Run Playwright against a local or staging target.
7. Run Gitleaks on the staged diff and repository history before any push.
8. Review changes and use a normal fast-forward commit/push.

## Network boundary

This project has no ports stanza and does not modify UFW/nftables, reverse proxy, DNS, NAT, or cloud firewall settings. Connect through already-existing private access paths. Never expose Docker socket, databases, model gateways or agent APIs directly to the public internet.

## Existing host caveats

- Root filesystem was observed at 89% use during the 2026-11-12 inspection.
- OpenHands and Dify are running; Dify agent_backend and local_sandbox were restarting at inspection.
- exa-mcp was restarting at inspection.
- The host has several pre-existing public listeners; this project adds none.
