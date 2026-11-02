#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# 全境 secret 掃描（open-hands repo）
# 1) 精確掃: 本 repo「自訂層」的檔案（vs upstream/main）— 命中即失敗
# 2) 全樹掃: 整個 working tree（排除 .git/node_modules/dist）— 僅資訊
# 用法: bash scripts/scan-secrets.sh
# ═══════════════════════════════════════════════════════════
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PATTERNS=(
  'sk-[A-Za-z0-9]{25,}'
  'nvapi-[A-Za-z0-9_-]{25,}'
  'alv2_[A-Za-z0-9_-]{25,}'
  'ghp_[A-Za-z0-9]{25,}'
  'github_pat_[A-Za-z0-9_]{35,}'
  'AKIA[0-9A-Z]{16}'
  '8658007204:[A-Za-z0-9]{20,}'
  'BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY'
)

FAIL=0

echo "═══ [1/2] 精確掃: 自訂層檔案 (vs upstream/main) ═══"
if git rev-parse --verify upstream/main >/dev/null 2>&1; then
  FILES=$(git diff --name-only upstream/main...HEAD 2>/dev/null)
else
  FILES=$(git ls-files deploy/ scripts/ 2>/dev/null)
fi
if [ -z "$FILES" ]; then
  echo "  (無自訂檔案或上游 ref 不存在，改掃全部 tracked 檔)"
  FILES=$(git ls-files)
fi
for pat in "${PATTERNS[@]}"; do
  for f in $FILES; do
    [ -f "$f" ] || continue
    hit=$(grep -nE "$pat" "$f" 2>/dev/null | head -3)
    if [ -n "$hit" ]; then
      FAIL=1
      echo "⚠️ [$f] pattern [$pat]:"
      echo "$hit" | sed -E "s/($pat)/***MASKED***/g"
    fi
  done
done
[ "$FAIL" = "0" ] && echo "  ✓ 自訂層無 secret 命中"

echo
echo "═══ [2/2] 全樹掃 (資訊, 排除 .git/node_modules/dist/build) ═══"
TOTAL=0
for pat in "${PATTERNS[@]}"; do
  HITS=$(grep -rInE --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=dist --exclude-dir=build \
        --exclude='*.min.js' --exclude='*.map' --exclude='*.lock' -E "$pat" . 2>/dev/null | head -5)
  if [ -n "$HITS" ]; then
    TOTAL=$((TOTAL+1))
    echo "  pattern [$pat]:"
    echo "$HITS" | sed -E "s/($pat)/***MASKED***/g"
  fi
done
[ "$TOTAL" = "0" ] && echo "  ✓ 全樹無命中"

echo
if [ "$FAIL" = "0" ]; then
  echo "✓ 掃描通過 — 可以推送"
  exit 0
else
  echo "✗ 自訂層發現 secret — 先處理再推送！"
  exit 1
fi
