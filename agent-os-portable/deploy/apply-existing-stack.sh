#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPENHANDS_DIR="${OPENHANDS_DIR:-/opt/agents/-/openhands}"
OPENHANDS_ENV="${OPENHANDS_ENV:-/opt/agents/-/.env}"
DIFY_DIR="${DIFY_DIR:-/opt/dify/docker}"
DIFY_RUNTIME_ENV="${DIFY_RUNTIME_ENV:-$HOME/.config/xiaye-agent-os/dify-runtime.env}"

for f in "$OPENHANDS_DIR/docker-compose.yml" "$OPENHANDS_ENV" "$DIFY_DIR/docker-compose.yaml" "$DIFY_DIR/.env" "$DIFY_RUNTIME_ENV"; do
  [[ -r "$f" ]] || { echo "Required file is missing or unreadable: $f" >&2; exit 2; }
done

docker compose --env-file "$OPENHANDS_ENV" \
  -f "$OPENHANDS_DIR/docker-compose.yml" \
  -f "$REPO_ROOT/deploy/openhands-litellm.override.yml" \
  up -d --no-deps litellm

docker compose --env-file "$DIFY_DIR/.env" --env-file "$DIFY_RUNTIME_ENV" \
  -f "$DIFY_DIR/docker-compose.yaml" \
  up -d --no-deps agent_backend local_sandbox
