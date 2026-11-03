# VPS portable migration status — 2026-10-29

## Newly pushed and verified

- hermes-007:migration-vps-portable-20261029 — 277e10b89dcbc0f85ea8d4a580812cc399b06114. Contains filtered portable tool/plugin source, selected installed workspace source, Hermes reference docs, config.yaml.example, config.json.example, and mcp-servers.json.example. Gitleaks staged scan passed after withholding five flagged paths. Live config, environment files, logs, backups, runtime state, and credentials were excluded.
- Cloud-vps:migration-agent-deployments-20261026 — f2ea40da0205d5434ebfa6d3e34fcfeafc7682a1. Includes the agent-plane compose file. Gitleaks staged scan passed.
- Both remote branch SHAs were checked against the intended commits after push.

## Pull

On a fresh machine, run:
  git clone --single-branch --branch migration-agent-deployments-20261026 https://github.com/tpisces88690/Cloud-vps.git
  cd Cloud-vps
  bash scripts/pull-agent-repositories.sh docs/PORTABLE_REPO_MANIFEST.tsv ./agent-repos

The script clones each manifest branch into its own directory, verifies the checkout SHA, and skips any destination directory that already exists. It does not reset or overwrite existing working trees. Private repositories require GitHub authentication on the target machine.

## Known exclusions

- Runtime credentials, live .env files, private keys, logs, backups, caches, PID/lease state, and scan-flagged files are not published.
- The open-hands-workspace bulk dirty count was caused by file mode changes across 7,652 files; no content diff was found in that batch, so those permission-only changes were not committed.
- Remote Desktop Commander still reports the VPS device offline; the pushes above were performed through Gateway instead.


## Latest portable updates (2026-10-29)

- Cloud-vps branch: migration-agent-plane-update-20261029. Includes portable agent-plane deployment source at portable-vps/agent-plane-source/ and SentinelX Cloud Core source/test additions under sentinelx-cloud-core/.
- Hermes config template branch: tpisces88690/hermes-007, migration-vps-config-portable-20261029, commit a43fa1bea6c695d68d0a7684e0ff93f6dbd9a500. Includes sanitized config.yaml.example and updated portability references.
- Backup directories, broken Caddy configurations, runtime virtual environments, and live credential files are excluded from the portable package.

- Hermes portable installed-code update: tpisces88690/hermes-007 branch migration-vps-portable-update-20261029, commit f2b17b575ec89daea40d9f75a7f94466c62c0b28. Includes the installed agent context-compression module, OAuth auth constants, Copilot auth, migration setup code, and a narrow allowlist for public OAuth identifiers/source labels flagged as generic-key false positives.
