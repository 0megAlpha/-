# AGENT//THRONE
Mobile-first AI Operations HUD for the Ai-Agent-Skill integration layer.

## Run
`./run.sh`
Default: http://127.0.0.1:8787/

The bridge is localhost-only and read-only by default. It exposes telemetry, safe observation commands, Agent registry, and an optional OpenAI-compatible provider. API keys are read only from environment variables.

## Modules
- 3D/2.5D neon cyberpunk HUD
- Mobile-first bottom navigation
- glass UI + particles
- CPU/RAM/disk/latency telemetry
- Agent mesh + provider fabric
- isolated Agent sessions
- read-only terminal observation
- 8 visual scenes
- timeline/orchestration surface
- Web Audio synthesizer
- WebM capture
- slash commands
- 8 core hubs
- PWA manifest/service worker

## Provider
Set AGENT_THRONE_PROVIDER_URL, AGENT_THRONE_MODEL and AGENT_THRONE_API_KEY without committing secrets.
For phone access use an authenticated reverse proxy or SSH tunnel; do not expose the raw bridge publicly.
## Slash
/status /agents /mesh /scene <name> /timeline /workspace /logs /help