#!/usr/bin/env bash
# 執行工作流主控（自動載入 .env）
set -a
[ -f "$(dirname "$0")/../.env" ] && . "$(dirname "$0")/../.env"
set +a
cd "$(dirname "$0")/.."
python3 workflows/main_pipeline.py "$@"
