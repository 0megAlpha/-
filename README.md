# Portable Agent Workspace

Repository: `0megAlpha/-`
Canonical branch: `vps-mirror/full-tree`
GitHub visibility currently reported by GitHub: **Public**.

This repository is the sole destination for portable Agent source, shared skills, plugins, MCP adapters, tools, functions, workflows, manifests, deployment templates and verification records.

## Architecture

- `openhands/`: primary software-engineering Agent, runtime integration and OpenHands-specific extensions.
- `hermes/`: Hermes Agent source and Hermes-specific integration.
- `agents/`: standalone Agent definitions and shared capability collections. Each Agent must have one canonical directory.
- `agents/Ai-agent-skill/`: shared framework-neutral Skills, Plugins, MCP adapters, Tools and Workflows. This is a shared capability library, not a second runtime.
- Existing top-level Agent directories such as `aider/`, `claude-code/`, `cline/`, `continue/`, `crush/`, `deepseek/`, `devin/`, `goose/`, `opencode/`, `openwebui/` and `swe-agent/` must be reconciled before any duplicate directory is added.

## Verified Git submodules

Only these two submodules are currently declared in `.gitmodules`:

| Path | Upstream |
|---|---|
| `openhands/core/` | https://github.com/OpenHands/OpenHands |
| `openhands/software-agent-sdk/` | https://github.com/OpenHands/software-agent-sdk |

Other source folders are not automatically submodules. Do not describe them as submodules unless the Git tree contains the corresponding gitlink and `.gitmodules` entry.

## Clone

```bash
git clone --recurse-submodules --branch vps-mirror/full-tree https://github.com/0megAlpha/-.git
```

## Security and portability

- Never commit live API keys, tokens, cookies, private keys, SSH material, `.env` files, database dumps, private sessions, runtime memory databases, sensitive logs or private model weights.
- Keep environment-variable names and sanitized example values only.
- Preserve upstream LICENSE and NOTICE files.
- Record source URL, upstream version/commit, license, install location and test evidence for every integrated capability.
- Shared capability code has one canonical copy; Agent-specific adapters reference it instead of vendoring duplicates.
- Keep original Git history; no force push or history rewrite.

## Status

This is an active migration and integration workspace, not a claim that every VPS asset has already been installed or validated. The requirements, blockers and current inventory are recorded in:

- [Conversation-wide Agent requirements](docs/CONVERSATION-WIDE-AGENT-REQUIREMENTS.md)
- [Agent portability and VPS reconciliation](docs/AGENT-PORTABILITY-AND-DEPLOYMENT.md)
- [Deployment status handoff](docs/DEPLOYMENT-STATUS-2026-11-05.md)

A legacy 23.8 MB Agent-skill archive remains in the repository root and has not yet been content- or secret-scanned. Do not treat it as verified portable content or redistribute it until inspected. The repository is currently Public, so all committed material must be treated as publicly readable.
