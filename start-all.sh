#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

echo "🚀 啟動 AI Agent 環境..."
if [[ -f "$ENV_FILE" ]]; then
  source "$ENV_FILE"
  echo "✅ .env 已載入"
else
  echo "⚠️  找不到 .env，複製模板: cp $SCRIPT_DIR/.env.template $SCRIPT_DIR/.env"
  echo "   不填 Key 時僅 Ollama 本地模型可用（需先安裝 ollama）"
fi

bash "$SCRIPT_DIR/litellm/start.sh"
sleep 2
echo ""
echo "📋 服務狀態："
curl -s http://localhost:4000/health >/dev/null 2>&1 \
  && echo "✅ LiteLLM :4000 正常" \
  || echo "❌ LiteLLM 未啟動，查看 $SCRIPT_DIR/logs/litellm.log"

echo ""
echo "🎯 Agent 指令（全部指向 LiteLLM :4000）："
for cmd in openhands claude opencode aider cn cline plandex goose gemini codex qwen; do
  command -v "$cmd" &>/dev/null && echo "  $cmd"
done
