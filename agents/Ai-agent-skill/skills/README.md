# AI Agent Skills — Shared Capability Library

This directory contains only framework-neutral Skills reusable by multiple independent Agents. It is not an Agent runtime and is not a dumping ground for Agent-specific plugins.

## Ownership
- OpenHands-only Skills live in `openhands/extensions/skills/`.
- Hermes-only Skills, plugins, adapters and workflows live inside `hermes/`.
- DSH-only Skills, plugins, profiles and tools live inside `dsh/`.
- Open WebUI pipes, functions and tools live inside `openwebui/`.
- AI Agent Fleet-specific Skills live in `agents/ai-agent-fleet/skills/`.
- Only reusable cross-Agent Skills belong here.

## Validation
Every Skill must have valid YAML frontmatter with `name` and `description`, source and license provenance, a complete procedure, and a representative invocation test. A directory name or placeholder `SKILL.md` is not proof of a working capability.
