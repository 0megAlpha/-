# VPS Agent Migration Status

Updated 2026-10-26.

## Verified target branches

| Repository | Branch | Verified commit |
|---|---|---|
| All-in | feat/iphone-first-hent-cockpit-20261010 | dd08a8acaab7 |
| Ai-Agent-Skill | migration-vps-update-20261026 | 7ccd02797e6d |
| ai-agent-stack | portable-20260924 | bedcf0a09b16 |
| open-hands | migration-vps-20261025 | a8613dba85c1 |
| open-hands workspace baseline | migration-workspace-base-20261026 | 519b07a2f561 |
| ai-agent-fleet | main | 78d07f06282c |
| Cloud-vps | migration-agent-deployments-20261026 | 86e37cc6f927 |
| hermes-007 | migration-vps-update-20261026 | b928ab708c79 |
| agents | main | 601e897b8815 |
| -oh-my-agent- | main | f824560ec40f |
| -DARPA-AIxCC- | main | 3556c7404c04 |
| claude-code-action | main | 6d9a9a8837dc |

## Included migration content

- Hermes source, agent definitions, skills, plugins, rules, commands and scripts, with a sanitized configuration example.
- Hermes Ultimate deployment scripts, plugin notes, and sanitized JSON/YAML configuration examples.
- SentinelX Cloud Core tracked source snapshot and safe agent-plane Caddy/dashboard configuration.
- Sanitized agent-plane Compose example.
- Agent and plugin repository branches/tags were pushed without force-pushing or deleting remote data.

## Safety and follow-up

- Raw environment files, credentials, private keys, logs, backups, runtime installs, caches and state snapshots are excluded.
- Local deletion in ai-agent-fleet was not committed.
- A source-only snapshot branch was used for the OpenHands workspace because its working tree had file-mode-only changes.
- Dedicated repositories for agent-plane, sentinelx-cloud-core and hermes-ultimate were not present, so their safe contents are preserved as subdirectories in existing repositories.
- Runtime status and detailed logs remain on the VPS under /root/migration-logs.

## Upstream source snapshots and runtime upgrade status

- open-hands branch upstream-v1.33.0: e7627196460f0982dcf5fc9d32ea890093fc65ad. This is the official v1.33.0 source tree snapshot (2,772 files), pushed without changing the deployed container.
- hermes-007 branch upstream-v0.22.5: 76545af266caefc175ca19444247b4e23e581a5c. This is the official v0.22.5 source tree snapshot (20,799 files), pushed without replacing the custom configuration branch.
- Hermes v0.22.5 is installed in an isolated worktree and its targeted gateway/auth tests pass. Live services are intentionally not restarted until the broader API-server compatibility suite finishes because the currently deployed tree has a local API-server patch.
- The OpenHands v1.33.0 container image tag is not available under the expected GHCR name. The current latest tag resolves to the same image digest as the running container; the live container remains healthy and was not replaced.

## Final live rollout result

Updated 2026-10-26 02:03 Asia/Taipei:
- Hermes v0.22.5 is now the active runtime for hermes-api and hermes-gateway, via systemd drop-ins.
- Both services are active with zero systemd restarts after rollout.
- Hermes API docs and OpenAPI endpoints on loopback port 8642 return HTTP 200; gateway health on loopback port 8643 returns HTTP 200.
- The previous Hermes installation and original config remain in place for rollback; no configuration file was deleted or overwritten by the rollout.
- Rollback script is kept locally at /root/migration-logs/hermes-v0225-rollback/restore-old-execstart.sh.
- Verified upstream source snapshot branches: open-hands/upstream-v1.33.0 at e7627196460f0982dcf5fc9d32ea890093fc65ad and hermes-007/upstream-v0.22.5 at 76545af266caefc175ca19444247b4e23e581a5c.
