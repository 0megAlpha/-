#!/usr/bin/env bash
# Ai-agent-skill 去敏推送：先掃密鑰 → commit → push（絕不 --force）
set -euo pipefail
cd "$(dirname "$0")/.."
MSG="${1:-feat: Ai-agent-skill 更新}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -q && git branch -M main
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ 未設定 origin。請執行："
  echo "   git remote add origin https://github.com/xh09411-web/Ai-agent-skill.git"
  exit 1
fi
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "❌ .env 已被追蹤，拒絕推送。"; exit 1
fi

echo "🔒 掃描密鑰..."
if [ -f ../All-in/core/security/key_manager.py ]; then
  python3 ../All-in/core/security/key_manager.py scan . || { echo "❌ 偵測到疑似密鑰，中止。"; exit 1; }
elif command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --no-git -v || { echo "❌ gitleaks 偵測到密鑰，中止。"; exit 1; }
else
  echo "⚠️ 無 gitleaks 也無 key_manager.py，跳過掃描（請人工檢查 diff）"
fi

git add -A
git commit -q -m "$MSG" || echo "（無新變更）"
if ! git push -u origin main; then
  echo "❌ 推送被拒。請先 git pull --rebase origin main；本腳本絕不 --force（P0 規則）。"
  exit 1
fi
echo "✅ 推送完成，commit hash：$(git rev-parse HEAD)"
