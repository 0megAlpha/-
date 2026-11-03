#!/usr/bin/env bash
# agent-system 環境準備
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"

echo "== [1/4] 建立 .env（若無）=="
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  已從 .env.example 複製 .env — 請填入真實值（LITELLM_MASTER_KEY 等）"
else
  echo "  .env 已存在，保留"
fi
chmod 600 .env 2>/dev/null || true

echo "== [2/4] 虛擬環境 =="
[ -d .venv ] || $PY -m venv .venv
. .venv/bin/activate
$PY -m pip install --quiet requests 2>/dev/null || echo "  (requests 安裝略過，stdlib 也可跑)"

echo "== [3/4] 語法檢查 =="
find agents workflows -name '*.py' -print0 | xargs -0 $PY -m py_compile
echo "  py_compile 全部通過"

echo "== [4/4] 目錄 =="
mkdir -p workflows/data workflows/state logs
echo "  workflows/data, workflows/state, logs 已建立"
echo ""
echo "✓ 完成。下一步: bash scripts/smoke_test.sh（mock 驗證流程）"
