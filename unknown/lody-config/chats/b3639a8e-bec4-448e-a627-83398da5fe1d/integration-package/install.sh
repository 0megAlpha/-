#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  DSH 技能整合安裝腳本（ai-agent-skill 儲存庫 → 本機 agent 技能庫）
#  沙盒內 /root/.agents/skills 為唯讀，請在 VPS 自己的 shell 執行：
#    bash /root/.lody/chats/b3639a8e-bec4-448e-a627-83398da5fe1d/integration-package/install.sh
#
#  用法：
#    bash install.sh                 # 安裝全部 34 個推薦技能
#    bash install.sh --list          # 列出套件內技能
#    bash install.sh --dry-run      # 預覽安裝內容，不實際寫入
#    bash install.sh <名稱> [名稱…]  # 只安裝指定技能（目錄名稱）
#    TARGET_DIR=/path bash install.sh        # 自訂安裝目標目錄
#    bash install.sh --force        # 覆蓋已存在的同名技能
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/skills"
TARGET_DIR="${TARGET_DIR:-$HOME/.agents/skills}"
DRY_RUN=0
FORCE=0
ONLY=()

for arg in "$@"; do
  case "$arg" in
    --list)    ls -1 "$SRC"; exit 0 ;;
    --dry-run) DRY_RUN=1 ;;
    --force)   FORCE=1 ;;
    -h|--help) grep '^#' "$0" | head -16; exit 0 ;;
    *)         ONLY+=("$arg") ;;
  esac
done

if [ ! -d "$SRC" ]; then
  echo "✗ 找不到技能來源目錄: $SRC" >&2; exit 1
fi

mkdir -p "$TARGET_DIR" 2>/dev/null || {
  echo "✗ 無法寫入目標目錄: $TARGET_DIR（若在 DSH 沙盒內，請改在你自己的 VPS shell 執行本腳本）" >&2
  exit 1
}

installed=0; skipped=0; failed=0
for skill_dir in "$SRC"/*/; do
  name="$(basename "$skill_dir")"
  [ -f "$skill_dir/SKILL.md" ] || { echo "  ⚠ $name 缺少 SKILL.md，略過"; continue; }
  if [ ${#ONLY[@]} -gt 0 ]; then
    match=0
    for o in "${ONLY[@]}"; do [ "$o" = "$name" ] && match=1; done
    [ $match -eq 1 ] || continue
  fi
  dst="$TARGET_DIR/$name"
  if [ -d "$dst" ] && [ $FORCE -eq 0 ]; then
    echo "  = 已存在，略過: $name（用 --force 覆蓋）"
    skipped=$((skipped+1)); continue
  fi
  if [ $DRY_RUN -eq 1 ]; then
    echo "  [預覽] $name"
    installed=$((installed+1)); continue
  fi
  rm -rf "$dst"
  if cp -r "$skill_dir" "$dst"; then
    echo "  ✓ 已安裝: $name"
    installed=$((installed+1))
  else
    echo "  ✗ 失敗: $name" >&2
    failed=$((failed+1))
  fi
done

echo "──────────────────────────────"
echo "安裝完成: $installed 個 | 略過: $skipped | 失敗: $failed"
echo "安裝目標: $TARGET_DIR"
[ $DRY_RUN -eq 1 ] && echo "（dry-run 模式，未實際寫入）"
echo "完成後請重啟 agent session，新技能才會出現在技能目錄中。"
exit 0
