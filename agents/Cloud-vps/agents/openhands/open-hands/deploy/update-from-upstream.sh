#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# 更新上游 OpenHands（保留官方更新通道）
# 用法: bash deploy/update-from-upstream.sh
# ═══════════════════════════════════════════════════════════
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== [1/5] fetch upstream =="
git fetch upstream main

echo "== [2/5] 檢查可更新 commit =="
BEHIND=$(git rev-list --count HEAD..upstream/main 2>/dev/null || echo 0)
if [ "$BEHIND" = "0" ]; then
  echo "✓ 已是最新 ($(git log -1 --format='%h %s'))"
  exit 0
fi
echo "上游有新 commit × $BEHIND"

echo "== [3/5] merge upstream/main =="
git merge --no-edit upstream/main || {
  echo "!! 衝突 — 手動解決後再: git commit / bash deploy/update-from-upstream.sh"
  exit 1
}

echo "== [4/5] secret 全境掃描（推送前強制）=="
bash scripts/scan-secrets.sh || { echo "!! 掃描有命中，中止"; exit 1; }

echo "== [5/5] 重建部署 =="
if [ -f docker-compose.override.yml ]; then
  docker compose up -d --build
else
  echo "（無 override，未重建 — 先 cp deploy/docker-compose.override.yml.template docker-compose.override.yml）"
fi

echo "✓ 更新完成: $(git log -1 --format='%h %s')"
echo "→ 用 Telegram bot /exec 或手動 push 到 private repo 備份"
