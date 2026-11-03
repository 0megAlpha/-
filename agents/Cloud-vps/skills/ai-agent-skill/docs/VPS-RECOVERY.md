# VPS Recovery and Portable Agent Fleet

Canonical source: private repository [xh09411-web/Ai-Agent-Skill](https://github.com/xh09411-web/Ai-Agent-Skill).

## Recover after VPS expiry

1. Provision a fresh supported Linux VPS and install Git and Python 3.
2. Restore provider/API credentials from your own password manager or secret manager. Never commit `.env`, API keys, SSH private keys, provider tokens, or LiteLLM master keys.
3. Authenticate to GitHub using a private-repository-capable credential. Prefer a short-lived fine-grained token or read-only deploy key for recovery.
4. Clone and validate the repository:

   ```bash
   git clone https://github.com/xh09411-web/Ai-Agent-Skill.git
   cd Ai-Agent-Skill
   python3 -m pip install PyYAML
   python3 tools/verify_repo.py
   bash -n deploy/portable-recovery.sh
   ```

5. Run `bash deploy/portable-recovery.sh` to print a plan. It does not overwrite existing agent skill files. Use `--apply` only after reviewing the plan.
6. Re-provision services from reviewed deployment manifests. Do not blindly replay old shell history or auto-run arbitrary third-party install scripts.
7. Verify firewall policy, listening sockets, service health, API authentication, model inference, and agent tool use before exposing any port.

## Port and secret policy

- Bind model gateways to loopback or a private overlay network by default.
- Do not expose LiteLLM, Qdrant, Docker API, SSH, agent control APIs, or dashboards directly to the public Internet without an authenticated reverse proxy and a reviewed firewall rule.
- Use distinct credentials per service, least-privilege scopes, rotation, and a secret manager.
- Treat a successful `/v1/models` response as discovery only; require an actual inference test.
- Never claim a service is healthy based solely on static dashboard metadata.
- Treat public repositories as untrusted source. Pin versions or commits and review install scripts before executing them.

## Recovery helper boundaries

The recovery helper does not install Docker, change firewall rules, start services, or configure provider keys. Those actions are environment-specific and must be performed from reviewed manifests and verified afterward. This keeps a replacement VPS from inheriting stale ports, leaked secrets, or broken service commands.
