# Agent Capability Ownership

This repository is public. Host-specific inventories, internal ports/IPs, secrets, runtime state, logs and raw snapshots are excluded.

- `openhands/`: OpenHands core, SDK, official Extensions source, and OpenHands-only Skills under `openhands/extensions/skills/`.
- `hermes/`: the complete Hermes Agent source, Hermes-only Skills, plugins, adapters and runtime templates.
- `dsh/`: DSH source, profile bundles, plugins, tools, ACP/MCP bridges and DSH-only Skills.
- `openwebui/`: Open WebUI source, pipes, functions, tools, plugins and adapters.
- `agents/ai-agent-fleet/`: AI Agent Fleet and its Fleet-specific Skills.
- `agents/Ai-agent-skill/skills/`: framework-neutral Skills reusable by multiple independent Agents.
- `ops/skills/`: host-neutral operations Skills; no host-specific credentials or infrastructure data.
- `shared/`: shared libraries, MCP contracts and adapters only; do not store Agent-specific plugins here.

A clone of each Agent directory must contain all of that Agent's own Plugins, Skills, Tools, Functions, MCP adapters, manifests, tests and install instructions. Shared assets may be referenced by ID and installed through the Agent's adapter, but must not be duplicated.

## Current move set

- OpenHands-specific Skills are stored in `openhands/extensions/skills/`.
- Framework-neutral Skills are stored in `agents/Ai-agent-skill/skills/`.
- AI Agent Fleet Skill is stored in `agents/ai-agent-fleet/skills/`.
- VPS bridge Skill is stored in `ops/skills/`.
- The `magic-word` test-only Skill is excluded from production packages.

## Validation status

File placement is a repository packaging step, not a runtime deployment claim. Each Skill still requires frontmatter validation, dependency/license review, source provenance, and an invocation test in its owning Agent.
