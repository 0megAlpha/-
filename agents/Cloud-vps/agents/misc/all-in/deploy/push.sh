#!/usr/bin/env bash
# 去敏推送：先掃密鑰 → commit → push（絕不 --force，遵守 P0 規則）
set -euo pipefail
cd "$(dirname "$0")/.."
MSG="${1:-feat: All-in 更新}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -q && git branch -M main
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ 未設定 origin。請執行："
  echo "   git remote add origin https://github.com/xh09411-web/All-in.git"
  exit 1
fi
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "❌ .env 已被 git 追蹤，拒絕推送。請執行：git rm --cached .env && git commit -m 'remove env'"
  exit 1
fi

echo "🔒 掃描密鑰（去敏檢查）..."
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --no-git -v || { echo "❌ gitleaks 偵測到疑似密鑰，中止推送。"; exit 1; }
else
  python3 core/security/key_manager.py scan . || { echo "❌ 掃描偵測到疑似密鑰，中止推送。"; exit 1; }
fi

git add -A
git commit -q -m "$MSG" || echo "（無新變更）"
if ! git push -u origin main; then
  echo "❌ 推送被拒（可能是非 fast-forward）。請先：git pull --rebase origin main，再重跑本腳本。"
  echo "   依專案 P0 規則，本腳本絕不使用 --force。"
  exit 1
fi
echo "✅ 推送完成，commit hash：$(git rev-parse HEAD)"
