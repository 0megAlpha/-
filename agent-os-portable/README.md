# Xiaye Agent OS

Portable engineering-agent workspace. OpenHands remains the code-execution agent; LangGraph provides bounded planning/review orchestration; LiteLLM provides an OpenAI-compatible model gateway. Dify remains the visual workflow surface. Aider is installed as an optional terminal pair-programmer. Playwright, pytest, Ruff, Semgrep, Trivy and Gitleaks provide verification.

## Principles
- No inbound port is created by this repository.
- No production service is restarted or replaced by bootstrap scripts.
- Secrets live in an untracked .env file or a secret manager; .env.example contains placeholders only.
- Review loops are bounded by MAX_REVIEW_CYCLES.
- OpenHands performs file changes only in an explicitly selected workspace. Back up and review diffs before merge.
- No force push, history rewrite, or automatic deletion of user files.

## Existing service integration
Use the existing LiteLLM OpenAI-compatible endpoint at http://127.0.0.1:14000/v1 and a model alias already configured there. OpenHands and Dify endpoints must match their installed versions; do not assume unsupported /execute routes.

## Install
Requires Python 3.12 and uv:
~~~bash
uv sync --extra dev
cp .env.example .env
uv run python -m agent_os.cli "Inspect this repository and propose a safe implementation plan"
uv run pytest
uv run ruff check .
~~~
Never commit .env.

## Workflow
1. Intake and inventory.
2. LangGraph planning and bounded review.
3. OpenHands execution in an isolated workspace.
4. Playwright, unit, lint and security checks.
5. Human review of diffs and explicit merge.
6. Commit and push to the selected 0megAlpha repository.

## OpenHands API execution
Installed web server is 0.47.0. A tested HTTP adapter uses the existing loopback API at port 13000; no new listener is created.
~~~bash
uv run python -m agent_os.cli --send-to-openhands --repository https://github.com/0megAlpha/- --branch agent-os/portable-core-2026-11-12 "Implement the approved task"
~~~
The official OpenHands SDK and tools 1.61.0 live in separate .venv-openhands because their certifi/psutil constraints conflict with Aider.
