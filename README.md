# Portable Agent Workspace

Repository: 0megAlpha/-
Canonical branch: vps-mirror/full-tree
Visibility last verified: Public.

This repository is the single portable source tree for the VPS Agent ecosystem. Each independent Agent must be pullable as one complete canonical directory, with its own source, runtime adapter, configuration templates, tools, Skills, Plugins, workflows, tests and deployment documentation.

## Canonical ownership
- openhands/: primary software-engineering Agent and OpenHands-specific runtime/extensions.
- hermes/: Hermes source, Hermes-specific Skills/Plugins, gateway adapters and deployment templates.
- dsh/: DeepSeek Harness source, profiles, plugins, tools and DSH-specific integrations.
- openwebui/: Open WebUI source/runtime integration, pipes, tools and UI plugins.
- agents/<agent-id>/: one complete directory per other independent Agent (Claude Code, OpenCode, Cline, Aider, Goose, Agent Plane, SentinelX, Agent-Throne, AI Agent Fleet, etc.).
- agents/Ai-agent-skill/: shared capability library only; not a dumping ground for Agent-specific plugins or packages.
- shared/: only genuinely cross-Agent code: LLM routing contracts, MCP registry/schema, shared adapters and common protocols.
- ops/: host-neutral templates and health checks. Host-specific secrets, live port maps, IPs, tokens and private runtime data are excluded.
- docs/: source documents, migration maps, architecture, provenance and verified runbooks.

## Packaging rule
A clone of openhands/, hermes/, dsh/, openwebui/ or agents/<agent-id>/ must contain that Agent's complete portable capability set. Shared Skills may be referenced by adapters/manifests, but Agent-specific Skills/Plugins/Tools must live inside their owning Agent directory. The shared capability library contains only assets verified as framework-neutral and reusable by multiple Agents. Do not put all extensions into one global skills folder.

## Upstream and history
- Keep upstream source, version/tag, license, commit provenance and local patches traceable.
- Preserve existing Git history, submodules and gitlinks where applicable.
- Never force-push or rewrite history.
- Do not flatten an upstream submodule into a second copy of the same source.
- Each Agent has one canonical folder; version snapshots and backups are kept inside that folder only when genuinely distinct and useful.

## Security and portability
This repository is currently Public. Never commit live API keys, tokens, cookies, passwords, private keys, SSH material, .env values, OAuth refresh tokens, database dumps, runtime sessions, private memory stores, sensitive logs, private model weights, host-specific port inventories, internal IPs or private deployment endpoints. Use sanitized .example templates with placeholder values only. Preserve upstream LICENSE/NOTICE files.

## Current migration status
This is an active reconciliation workspace, not a claim that every VPS asset has been mirrored or every Agent is runtime-verified. Each component must record source, canonical owner, install target, version/commit, secret-scan result, tests and remote commit SHA before being marked complete.

Current evidence and remaining work:
- docs/AGENT-CAPABILITY-OWNERSHIP.md
- docs/AGENT-CAPABILITY-OWNERSHIP.md
