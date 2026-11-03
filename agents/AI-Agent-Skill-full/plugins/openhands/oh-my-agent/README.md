# OH-MY-AGENT (selectable OpenHands MCP plugin)

This is a small stdio MCP server, not a claim that a full self-evolving platform is already deployed. It exposes explicit tools to OpenHands/compatible MCP clients: status, OpenAI-compatible provider probe, skill inventory, sanitized draft creation, Mem0 search/store, upstream metadata checks, and a fail-closed promotion checklist.

## Install in an isolated environment

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ./extensions/plugins/oh-my-agent
```

The package exposes `oh-my-agent-mcp` as its MCP stdio command. Configure the OpenHands Agent Plugins/MCP client using the supported configuration format for your deployed OpenHands version, with command `oh-my-agent-mcp`. Keep the process inside the agent's existing sandbox; do not mount the host Docker socket or production credentials into evolution workers.

## Environment

- `LLM_BASE_URL` (or `OPENAI_BASE_URL`) and `LLM_API_KEY` (or `OPENAI_API_KEY`) for `/models` probe.
- `MEM0_URL` and optional `MEM0_API_KEY` for Mem0 API operations.
- `OHMA_SKILL_ROOTS` (path-separator-delimited, default `.agents/skills:skills`) for read-only skill listing.
- `OHMA_DRAFT_ROOT` (default `.oh-my-agent/drafts`) for new draft skills. Drafts are mode 0600 where supported and are never auto-installed.

Never put secrets in this repository, tool output, skill text, or issue comments. Use environment injection/secret manager. The plugin does not pull or execute third-party skill code.

## Tools

- `system_status`
- `provider_probe`
- `skills_list`
- `skill_draft_create`
- `memory_search`
- `memory_store`
- `upstream_status`
- `promotion_check`

`promotion_check` is evidence-only and always returns `promotion_allowed: false`; human review and a separately implemented deployment workflow are still required. This is intentional.

## Local verification

```bash
python -m unittest discover -s tests -v
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}' | oh-my-agent-mcp
```

No production deployment is performed by installation or by these tools.
