# Devin service integration

Devin is a hosted agent service, not a locally configured model runner. Use Devin's documented service API and MCP integrations to create tasks, inspect sessions, and connect external tools. Keep DEVIN_API_KEY in the secret manager. Do not add OPENAI_BASE_URL or claim that Devin can route its internal inference through arbitrary self-hosted endpoints unless the current Devin contract explicitly exposes that feature.
