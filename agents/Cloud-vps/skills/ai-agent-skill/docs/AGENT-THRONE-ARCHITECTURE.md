# AGENT//THRONE Architecture
Ai-Agent-Skill is the integration/skills/adapter/workflow layer. Source runtimes stay independent.

Canonical boundaries:
- Hermes: /root/007-hermes
- OpenHands: /root/open-hands
- OpenCode: /root/opencode
- Claude Code: /root/AI-Agent-Skill/agents/claude-code
- DSH: installed runtime + /root/--dsh
- Agents ecosystem: /root/agents
- Ai-Agent-Skill: /root/ai-agent-skill

Session routing key:
agent_id + workspace_id + session_id + provider_id + model_id

Provider types:
OpenAI-compatible HTTP / ACP stdio / local HTTP / CLI.
A shared provider does not imply shared conversation history.

Default bridge:
GET /api/health
GET /api/status
GET /api/agents
GET /api/observe?kind=status|ps|ports|git
POST /api/chat

Security:
- localhost bind by default- read-only observer
- no generic shell endpoint
- secrets only from environment
- no hidden persistence
- no automatic external offensive execution

Future mutating actions must be explicit adapters with validation, audit records, stoppable process groups and least privilege.

Browser-capable agents use isolated browser storage/session IDs; never share a credential jar implicitly.