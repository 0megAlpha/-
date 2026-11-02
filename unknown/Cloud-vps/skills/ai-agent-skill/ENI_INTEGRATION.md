# ENI / Agent Integration Snapshot

This repository stores integration metadata only. Runtime endpoints and credentials are deployment configuration, not source-controlled data.

Integrated adapter targets:
- DSH
- OpenHands
- OpenCode
- Hermes
- Claude Code
- Cline / ACP
- OpenWebUI
- Lody
- Conduit

Provider contract:
- OpenAI-compatible HTTP
- LiteLLM gateway
- local llama.cpp HTTP
- ACP stdio

Security:
- no API keys in Git
- no private network addresses in public documentation
- per-agent session isolation
- explicit adapter permissions
- no hidden persistence
