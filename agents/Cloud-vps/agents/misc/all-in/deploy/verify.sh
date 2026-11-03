#!/usr/bin/env bash
# All-in 服務驗證 —— 只回報事實，不偽造狀態
TS_IP="${TS_IP:-100.x.x.x}"
pass=0; fail=0

chk() { # $1=名稱 $2=URL
  code=$(curl -s -o /dev/null -m 5 -w '%{http_code}' "$2" 2>/dev/null || true)
  if [ "$code" = "200" ]; then
    echo "  ✅ $1 ($2)"; pass=$((pass+1))
  else
    echo "  ❌ $1 ($2) → HTTP ${code:-000}"; fail=$((fail+1))
  fi
}

echo "=== All-in 驗證（$(date '+%F %T')）==="
chk "Hermes :8642（Tailscale）" "http://$TS_IP:8642/health"
chk "Hermes :8642（本機）"      "http://127.0.0.1:8642/health"
chk "Qdrant :6333"              "http://127.0.0.1:6333/healthz"
chk "Open WebUI :3000"          "http://127.0.0.1:3000/health"
chk "Mem0 :8000"                "http://127.0.0.1:8000/health"
chk "OpenHands :18000"          "http://127.0.0.1:18000/health"

echo "Skills 載入數：$(ls -1 "$HOME/.hermes/skills" 2>/dev/null | wc -l)"

if python3 - <<'PY' 2>/dev/null
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/sesm"))
from sesm_engine import SESMUltimateEngine
print("  ✅ SESM 引擎可載入")
PY
then :; else echo "  ❌ SESM 引擎載入失敗（檢查 python3 / pip install requests qdrant-client / .env）"; fi

echo "=== 驗證完成：$pass OK / $fail FAIL ==="
