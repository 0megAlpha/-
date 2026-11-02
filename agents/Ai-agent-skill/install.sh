#!/usr/bin/env bash
# Ai-agent-skill 冪等安裝：技能 → 三個 Agent 的 skills 目錄；references → ~/.agents/references
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

for t in "$HOME/.agents/skills" "$HOME/.hermes/skills" "$HOME/.config/opencode/skills"; do
  mkdir -p "$t"
done

SRC="$HERE/../All-in/skills"
if [ -d "$SRC" ]; then
  for t in "$HOME/.agents/skills" "$HOME/.hermes/skills" "$HOME/.config/opencode/skills"; do
    cp -r "$SRC/." "$t/"
  done
  echo "✅ 9 個技能已安裝到 ~/.agents/skills、~/.hermes/skills、~/.config/opencode/skills"
else
  echo "⚠️ 找不到 $SRC（請把 All-in 倉庫放在隔壁目錄，技能本體在那裡）"
fi

mkdir -p "$HOME/.agents/references"
cp -r "$HERE/references/." "$HOME/.agents/references/" 2>/dev/null || true
echo "✅ 共享 references → ~/.agents/references/"
echo "安裝統計："
echo "  ~/.agents/skills：$(ls -1 "$HOME/.agents/skills" 2>/dev/null | wc -l) 項"
echo "  ~/.hermes/skills：$(ls -1 "$HOME/.hermes/skills" 2>/dev/null | wc -l) 項"
