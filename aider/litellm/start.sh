#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"
[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"
pkill -f "litellm.*4000" 2>/dev/null || true
sleep 1
nohup litellm --config "$SCRIPT_DIR/config.yaml" --port 4000 \
  > "$SCRIPT_DIR/../logs/litellm.log" 2>&1 &
echo "LiteLLM 啟動中... http://localhost:4000"
sleep 4
curl -s http://localhost:4000/health 2>/dev/null | head -c 500 || echo "等待啟動..."
