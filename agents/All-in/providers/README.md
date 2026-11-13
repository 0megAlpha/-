# All-in orchestration bundle provider adapter

Canonical path: `agents/All-in`. This is a multi-agent orchestration bundle, not a separate standalone LLM agent. It coordinates child runtimes and already exposes provider endpoint variables in its root `.env.example`.

Supported endpoint variables include:
- `OPENAI_BASE_URL`
- `DEEPSEEK_BASE_URL`
- `MOONSHOT_BASE_URL`
- `OPENROUTER_BASE_URL`
- `LITELLM_ENDPOINT`

For the VPS LiteLLM gateway, use `http://agents-litellm:4000` on the Docker network or `http://127.0.0.1:14000` on the host. Keep child Agent credentials and provider settings in each child Agent's own directory; All-in should only carry orchestration-level service endpoints and runtime secrets.

`agents/All-in-root` is a divergent historical snapshot containing additional security/deployment files and changed Compose/dashboard files. It is retained for comparison and is not a second deployment target. Merge its unique files into the canonical All-in directory only after file-by-file review; do not overwrite the canonical tree wholesale.
