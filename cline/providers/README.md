# Cline Provider Adapter

Configure this in Cline's provider settings (OpenAI Compatible):
- Base URL: `http://127.0.0.1:14000/v1` on the VPS host, or the gateway's service DNS name inside its Docker network.
- API key: runtime secret mapped to `OPENAI_API_KEY`.
- Model ID: an exact model alias from the gateway's model list.
- Enable streaming and tool/function calling only when the selected provider supports them.

Cline settings are managed by its own UI/config store. This directory contains the reproducible setup contract, not a fake settings file.
