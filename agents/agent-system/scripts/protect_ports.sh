#!/usr/bin/env bash
# 端口保護：審計 + 套用 OpenWebUI 註冊防護
# 用法: bash scripts/protect_ports.sh [apply|audit]
set -u
ACTION="${1:-audit}"
OW_DATA=/root/ai-company/open-webui

echo "== 審計：本機端口認證層 =="
for p in 3000 4096 8080 4000; do
  echo -n "  localhost:$p -> "
  curl -s -o /dev/null -w '%{http_code}' --max-time 4 "http://localhost:$p/" 2>/dev/null || echo -n 'no-resp'
  echo
done

echo "== OpenWebUI 使用者狀態 =="
if [ -f "$OW_DATA/webui.db" ]; then
  python3 - "$OW_DATA/webui.db" << 'PY'
import sqlite3, sys
db = sys.argv[1]
try:
    con = sqlite3.connect(db)
    cur = con.cursor()
    n = cur.execute("select count(*) from user").fetchone()[0]
    roles = cur.execute("select role, count(*) from user group by role").fetchall()
    print(f"  users: {n} | roles: {roles}")
    con.close()
except Exception as e:
    print(f"  (無法讀 db: {e})")
PY
else
  echo "  (無 webui.db — 尚未建立管理員?)"
fi

if [ "$ACTION" = "apply" ]; then
  echo "== 套用：確認 open-webui 容器環境 =="
  docker inspect open-webui 2>/dev/null | python3 -c '
import json,sys
d=json.load(sys.stdin)[0]
envs=[e for e in d["Config"]["Env"]]
print("  ENABLE_SIGNUP:", [e for e in envs if "ENABLE_SIGNUP" in e] or "未設定（預設 true → 需關閉）")
'
  echo "  提示: 管理員已建立後，可將容器環境加 ENABLE_SIGNUP=false 阻擋匿名註冊。"
fi
