#!/usr/bin/env bash
set -euo pipefail
uv run pytest
uv run ruff check .
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks dir . --redact --no-banner
fi
