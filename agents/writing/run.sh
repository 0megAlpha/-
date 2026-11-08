#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"
export OPENHANDS_SKILLS_DIR="$DIR/skills"
export OPENHANDS_MCP_CONFIG="$DIR/config/mcp.json"
echo "[writing] skills=$(ls "$DIR/skills" | wc -l)  dir=$OPENHANDS_SKILLS_DIR"
if command -v openhands >/dev/null 2>&1; then
  case "${1:-web}" in
    web)   exec openhands web   --skills-dir "$OPENHANDS_SKILLS_DIR" --mcp-config "$OPENHANDS_MCP_CONFIG" ;;
    serve) exec openhands serve --skills-dir "$OPENHANDS_SKILLS_DIR" ;;
    *) echo "用法: $0 [web|serve]" ;;
  esac
else
  echo "OpenHands CLI 未装；在 Canvas → Settings → Skills 载入 $OPENHANDS_SKILLS_DIR"
fi
