#!/usr/bin/env bash
# 冒煙測試：不需要任何真實金鑰即可驗證全流程
set -euo pipefail
cd "$(dirname "$0")/.."
PY=python3
FAIL=0

echo "== [1/3] py_compile 全部 =="
find agents workflows -name '*.py' -print0 | xargs -0 $PY -m py_compile
echo "  OK"

echo "== [2/3] mock 管線執行（default）=="
export MOCK_LLM=1
OUT=$($PY workflows/main_pipeline.py --pipeline default --query "測試資料鏈接" 2>&1)
echo "$OUT" | tail -12
echo "$OUT" | grep -q "執行順序" && echo "  OK: 管線有產出" || { echo "  FAIL"; FAIL=1; }

echo "== [3/3] 產物與安全檢查 =="
ART=$(echo "$OUT" | grep -oP '產物: \K\S+' | head -1)
if [ -n "${ART:-}" ] && [ -f "$ART" ]; then
  echo "  產物: $ART ($(wc -c < "$ART") bytes)"
  if grep -qE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|alv2_[A-Za-z0-9_-]{20,}|205\.189\.160\.' "$ART"; then
    echo "  FAIL: 產物含 secret/IP"
    FAIL=1
  else
    echo "  OK: 產物無 secret"
  fi
else
  echo "  WARN: 找不到產物（dry-run?）"
fi

[ "$FAIL" = "0" ] && echo "✓ SMOKE TEST PASSED" || echo "✗ SMOKE TEST FAILED"
exit $FAIL
