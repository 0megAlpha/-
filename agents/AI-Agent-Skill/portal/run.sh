#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export AGENT_THRONE_HOST="${AGENT_THRONE_HOST:-127.0.0.1}"
export AGENT_THRONE_PORT="${AGENT_THRONE_PORT:-8787}"
echo "AGENT//THRONE: http://${AGENT_THRONE_HOST}:${AGENT_THRONE_PORT}/"
exec python3 server.py
