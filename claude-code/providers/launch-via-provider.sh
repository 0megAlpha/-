#!/usr/bin/env bash
set -euo pipefail
: "${ANTHROPIC_BASE_URL:?Set ANTHROPIC_BASE_URL in the runtime secret store}"
: "${ANTHROPIC_AUTH_TOKEN:?Set ANTHROPIC_AUTH_TOKEN in the runtime secret store}"
exec claude "$@"
