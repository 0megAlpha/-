#!/usr/bin/env bash
# ============================================================
# 修復 3/4：Harness 進化框架 —— clone SWE-agent / mini-swe-agent
# 到 ~/.hermes/skills/harness-evolution/src/，並確保不入庫（.gitignore）
# 官方 repo 拿不到時：請到 GitHub 搜尋同名專案，把 URL 填進 REPOS 再重跑。
# ============================================================
set -uo pipefail
DEST="$HOME/.hermes/skills/harness-evolution/src"
mkdir -p "$DEST"

REPOS=(
  "https://github.com/SWE-agent/SWE-agent.git"
  "https://github.com/SWE-agent/mini-swe-agent.git"
)

ok=0
for url in "${REPOS[@]}"; do
  name=$(basename "$url" .git)
  if [ -d "$DEST/$name/.git" ]; then
    echo "↻ 已存在：$DEST/$name"
    ok=$((ok+1)); continue
  fi
  if git clone --depth 1 "$url" "$DEST/$name" 2>/dev/null; then
    echo "✅ clone：$url"
    ok=$((ok+1))
  else
    echo "❌ clone 失敗：$url（請確認網路 / repo 是否改名，更新 REPOS 後重跑）"
  fi
done

[ "$ok" -eq ${#REPOS[@]} ] || echo "⚠️ 有 repo 未取得：請到 GitHub 搜尋 'SWE-agent' / 'mini-swe-agent'，把新 URL 填回本腳本。"

# 確保 clone 目錄不入庫（skill 目錄 + All-in 倉庫雙保險）
printf 'src/\n' > "$HOME/.hermes/skills/harness-evolution/.gitignore"
echo "✅ 已寫入 $HOME/.hermes/skills/harness-evolution/.gitignore（src/ 不入庫）"
echo "ℹ All-in/.gitignore 亦已包含 **/harness-evolution/src/"
echo ""
echo "已安裝內容："
ls -1 "$DEST" 2>/dev/null || true
