#!/usr/bin/env bash
set -euo pipefail
agent="${1:?agent id}"; gen="${2:?generation}"; root="$(cd "$(dirname "$0")" && pwd)"; out="$root/iterations/$agent/$gen"; mkdir -p "$out"; date -Is > "$out/started-at"; printf '{"agent_id":"%s","generation":%s,"parent":null,"fitness":0,"changes":[],"verification":"PENDING"}\n' "$agent" "$gen" > "$out/manifest.json"; echo "EVOLUTION_BASELINE $agent generation=$gen"; echo "Use sandboxed evaluation before promotion." > "$out/STATUS";
