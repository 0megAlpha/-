# Integration registry

| Tool | Role | State at inspection |
|---|---|---|
| OpenHands | coding/runtime agent | Existing container running; REST adapter for 0.47.0 tested |
| LiteLLM | model router | Existing container running; API config issue requires diagnosis |
| Dify | workflow UI | Existing deployment; agent backend and local sandbox restarting |
| LangGraph | orchestration | Installed and pinned in project |
| AutoGen / Magentic-One | multi-agent patterns | AutoGen modules present in system Python |
| Aider | terminal coding assistant | Installed in isolated project environment |
| Playwright | browser automation | Package installed; browser test setup available |
| pytest / Ruff | test and lint | Installed |
| Semgrep / Trivy / Gitleaks | security scanning | Tool availability found; full scans pending |
| GitHub | version control | Authenticated as 0megAlpha; destination 0megAlpha/- |
| Notion | operations record | Workspace connected |
| Vercel | deployment | Team scope requires approval; projects not verified |
| Shellway | remote workstation | Device offline |
| SentinelX | remote agent/security | Enrollment pending; no connected host |
| Termalin | remote host operations | Pro-only host listing unavailable on current plan |
| ButlerBrain | persistent memory | Connector tools available; account access to verify |
| Simplified | content workflow | Connector available; workspace access to verify |
| Searcherries | SEO analytics | Account and data-source access to verify |
| Replit | app workspace | No apps returned in prior check |
| MagicPath | UI prototyping | Connector available; project access to verify |
| Exa | search MCP | VPS container restarting at inspection |
| TinyFish / Firecrawl / Tavily / Parallel | research/browser | ChatGPT connectors available; not equivalent to VPS credentials |
| Lody | mobile coding-agent control | systemd service exists; CLI device authorization required |
| Conduit | mobile client | Open WebUI healthy on existing port 3000; client pairing not completed |

## Version compatibility
OpenHands web server 0.47.0; SDK/tools 1.61.0 in .venv-openhands. Aider's certifi/psutil pins conflict with OpenHands tools, so they remain in separate environments.
