#!/usr/bin/env bash
set -o pipefail; cd "${OPENHANDS_PROJECT_DIR:-.}"
find . -name "*.py" -not -path "./.venv/*" -print0 | xargs -0 -r python3 -m py_compile || { echo '{"decision":"deny","reason":"py_compile failed."}'; exit 2; }
command -v semgrep >/dev/null && semgrep --config=auto --error --quiet . || { echo '{"decision":"deny","reason":"semgrep issues."}'; exit 2; }
command -v bandit >/dev/null && bandit -q -r . -x .venv || { echo '{"decision":"deny","reason":"bandit issues."}'; exit 2; }
[ -f pytest.ini ] || [ -f pyproject.toml ] && pytest -q || { echo '{"decision":"deny","reason":"tests failed."}'; exit 2; }
exit 0
