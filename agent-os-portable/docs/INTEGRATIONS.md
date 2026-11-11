# Integration registry

| Tool | Role | Local integration state |
|---|---|---|
| OpenHands | coding/runtime agent | existing container running |
| LiteLLM | model router | existing container running |
| Dify | workflow UI | existing deployment; some containers restarting |
| LangGraph | primary stateful orchestration | installed in system Python; pinned in this project |
| AutoGen / Magentic-One | optional multi-agent patterns | AutoGen modules present in system Python |
| Aider | terminal coding assistant | install in isolated project venv |
| Playwright | browser automation | existing CLI/package present; Python dependency declared |
| pytest / Ruff | test and lint | existing tools present |
| Semgrep / Trivy / Gitleaks | security scanning | existing CLI tools present |
| GitHub | version control | OAuth connected as 0megAlpha |
| Notion | operations record | workspace connected |
| Vercel | web deployment | no connected teams/projects returned |
| Shellway | remote workstation execution | device reported offline at latest check |
| SentinelX | remote agent/security | no enrolled hosts; Free plan |
| Termalin | remote host operations | Free plan; host listing requires Pro |
| ButlerBrain | persistent memory | trial ended / upgrade required in prior record |
| Simplified | content workflow | workspace connected per operations record |
| Searcherries | SEO analytics | GitHub project exists; GA4/Search Console not connected |
| Replit | app workspace | no apps returned in prior record |
| MagicPath | UI prototyping | personal account available; no team reported |
| Exa | search MCP | container restarting at inspection |
| TinyFish / Firecrawl / Tavily / Parallel | research/browser connectors | available as ChatGPT tools; not VPS-hosted credentials |
| Lody | mobile coding-agent control | lody-agent.service active and CLI 0.103.0 installed; CLI is not authenticated yet, device authorization pending |
| Conduit | native Open WebUI / Hermes / OpenAI-compatible client | Open WebUI 0.13.3 healthy on existing port 3000; mobile pairing is user-side and not yet completed |

Connector presence is not equivalent to authenticated account linkage. Re-check each provider before automating account-level operations.
