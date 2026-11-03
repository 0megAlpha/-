# VPS Hermes migration snapshot

Date: 2026-10-29
Destination: tpisces88690/007-hermes, branch main

## Included

- The Hermes source tree, application and agent modules, tests, installer and packaging files, documentation, bundled skills, and plugin integrations from the source snapshot.
- A portable snapshot of the installed Hermes workspace under portable-installs/76f6e7e5145b5f39/workspace.
- Sanitized YAML, JSON, and MCP server configuration templates at config.yaml.example, config.json.example, and mcp-configs/mcp-servers.json.example.
- Portable restore notes, a toolchain inventory, and selected installed-tool source under portable-installs.
- Selected portable tool source, package manifests, documentation, and deployment configurations under portable-installs/tool-source.

## Security and portability boundaries

Live config.yaml/config.json, authentication files, MCP server credentials, runtime state, logs, caches, backups, and local state snapshots are excluded. The repository ignore rules keep these items out of future commits. Supply credentials on the destination host through environment variables or a secret manager; do not commit real keys or tokens.

Large bundled executables are not included because GitHub rejects individual files above 100 MiB. portable-installs/TOOLCHAIN-MANIFEST.md records the locally installed tool bundles; use the project bootstrap/install scripts and documentation to reinstall them on another host.

The destination repository was empty, so main is a sanitized source snapshot with a new root commit. Prior Git ancestry was not imported into this repository to avoid transferring unverified historical secrets. The original hermes-007 repository retains its separate history.

## Restore outline

1. Clone this repository on the destination host.
2. Create and activate a Python virtual environment.
3. Install the project from its packaging metadata and follow the main README for system dependencies.
4. Copy config.yaml.example to a local config.yaml only when required by the runtime; populate credentials locally and keep that file untracked.
5. Install the toolchain using the documented bootstrap/install scripts, then run the project smoke tests before enabling services.
