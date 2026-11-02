#!/usr/bin/env bash
# All-in 安裝：skills → ~/.hermes/skills、SESM → ~/.hermes/sesm、docker 基礎服務
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  cp .env.example .env
  echo "⚠️ 已建立 .env。請先填入真實 API Key（OPENROUTER/DEEPSEEK/MOONSHOT 至少一個）後重跑本腳本。"
  exit 1
fi

echo "🚀 [1/4] 部署 Skills → ~/.hermes/skills"
mkdir -p "$HOME/.hermes/skills" "$HOME/.hermes/sesm" "$HOME/.hermes/logs"
cp -r skills/. "$HOME/.hermes/skills/"

echo "🚀 [2/4] 部署 SESM 引擎 → ~/.hermes/sesm"
cp core/sesm_engine.py core/orchestrator.py core/agent_registry.json "$HOME/.hermes/sesm/"
if [ -f requirements.txt ]; then
  pip install -q -r requirements.txt 2>/dev/null || echo "⚠️ pip 安裝失敗（可手動：pip install -r requirements.txt）"
fi

echo "🚀 [3/4] 啟動 Docker 基礎服務（Qdrant / Mem0 / Open WebUI）"
if command -v docker >/dev/null 2>&1; then
  docker compose up -d || echo "⚠️ docker compose 失敗（可能已在運行或需 sudo / 重新登入取得 docker 群組）"
else
  echo "⚠️ 未安裝 docker，跳過（Qdrant/Mem0/Open WebUI 不會啟動）"
fi

echo "🚀 [4/4] 執行驗證"
bash deploy/verify.sh || true
echo "✅ 安裝完成。下一步：bash deploy/fix/01-fix-hermes-binding.sh"
