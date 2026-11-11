# Xiaye Agent OS

Portable engineering-agent workspace. OpenHands remains the code-execution agent; LangGraph provides bounded planning/review orchestration; LiteLLM provides an OpenAI-compatible model gateway. Dify remains the visual workflow surface. Aider is installed as an optional terminal pair-programmer. Playwright, pytest, Ruff, Semgrep, Trivy and Gitleaks provide verification.

## Principles

- No inbound port is created by this repository.
- No production service is restarted or replaced by the bootstrap scripts.
- Secrets live in an untracked .env file or a secret manager; .env.example contains placeholders only.
- Review loops are bounded by MAX_REVIEW_CYCLES; never run an unbounded autonomous loop.
- OpenHands performs file changes only in an explicitly selected workspace. Back up and review diffs before merge.
- No force push, no history rewrite, no automatic deletion of user files.

## Existing service integration

Configure OPENAI_API_BASE to the existing LiteLLM OpenAI-compatible endpoint and OPENAI_MODEL to a model alias already configured there. The default host-local endpoint is http://127.0.0.1:14000/v1; change it only if the actual deployment endpoint differs.

OPENHANDS_BASE_URL and DIFY_BASE_URL are integration references, not an invented /execute API. Use the API routes documented by the exact installed versions and keep credentials in local environment variables.

## Install

Requires Python 3.12 and uv:

~~~bash
uv sync --extra dev
cp .env.example .env
# Edit .env locally; do not commit it.
uv run python -m agent_os.cli "Inspect this repository and propose a safe implementation plan"
uv run pytest
uv run ruff check .
~~~

Aider is installed in the isolated project environment. Use uv run aider --help to verify the CLI.

## Workflows

1. Intake and inventory.
2. LangGraph planning and bounded review.
3. OpenHands execution in an isolated workspace.
4. Playwright / unit / lint / security checks.
5. Human review of diffs and explicit merge.
6. Git commit and push to the selected 0megAlpha repository.

The workflow definitions in workflows/ are orchestration contracts; they do not assume unsupported Dify/OpenHands endpoints.

## Lody / Conduit

The host has a lody-agent systemd service in the existing VPS inventory. This repository does not assume that a separately named Lody Conduit mobile app exposes an API. Keep app-specific endpoints and tokens out of this repo until verified from the installed app's official documentation.
