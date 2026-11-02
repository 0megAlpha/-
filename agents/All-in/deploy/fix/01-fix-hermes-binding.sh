#!/usr/bin/env bash
# ============================================================
# 修復 1/4：Hermes 8642 對 Tailscale 可達
# 流程：備份 .env → 改 API_SERVER_HOST → 重啟 hermes-gateway → curl 驗證 200
#       → 仍未通過則輸出 Nginx 反向代理備案（不自動安裝）
# 安全提醒：0.0.0.0 會對「所有介面」監聽；務必執行 core/security/firewall_rules.md
#           的 ufw 規則，或改用更保守的 API_SERVER_HOST=$TS_IP。
# ============================================================
set -uo pipefail
ENV_FILE="${HERMES_ENV:-$HOME/.hermes/.env}"
TS_IP="${TS_IP:-100.126.48.60}"
PORT="${HERMES_PORT:-8642}"

[ -f "$ENV_FILE" ] || { echo "❌ 找不到 $ENV_FILE（Hermes 未安裝於此帳號，或路徑不同）"; exit 1; }

TS=$(date +%Y%m%d-%H%M%S)
cp "$ENV_FILE" "$ENV_FILE.bak.$TS" && echo "🛡 已備份：$ENV_FILE.bak.$TS"

if grep -q '^API_SERVER_HOST=127\.0\.0\.1' "$ENV_FILE"; then
  sed -i 's/^API_SERVER_HOST=127\.0\.0\.1/API_SERVER_HOST=0.0.0.0/' "$ENV_FILE"
  echo "✅ API_SERVER_HOST：127.0.0.1 → 0.0.0.0"
elif grep -q '^API_SERVER_HOST=' "$ENV_FILE"; then
  echo "ℹ API_SERVER_HOST 目前為：$(grep '^API_SERVER_HOST=' "$ENV_FILE")（非 127.0.0.1，不重複修改）"
else
  printf 'API_SERVER_HOST=0.0.0.0\n' >> "$ENV_FILE"
  echo "✅ 已新增 API_SERVER_HOST=0.0.0.0"
fi

echo "⚠️ 建議：0.0.0.0 + ufw（僅放行 tailscale0）；或直接改用 API_SERVER_HOST=$TS_IP"

if sudo -n systemctl restart hermes-gateway.service 2>/dev/null; then
  echo "✅ 已重啟 hermes-gateway.service（sudo）"
elif systemctl restart hermes-gateway.service 2>/dev/null; then
  echo "✅ 已重啟 hermes-gateway.service"
else
  echo "⚠️ systemctl 重啟失敗：請手動執行 sudo systemctl restart hermes-gateway.service 後重跑本腳本驗證段落"
fi

for i in $(seq 1 10); do
  code=$(curl -s -o /dev/null -m 3 -w '%{http_code}' "http://$TS_IP:$PORT/health" 2>/dev/null || true)
  if [ "$code" = "200" ]; then
    echo "✅ http://$TS_IP:$PORT/health → 200（修復 1 完成）"
    exit 0
  fi
  sleep 2
done

echo "⚠️ 仍未回 200。Nginx 反向代理備案（只輸出設定檔內容，不自動安裝）："
cat <<EOF
# /etc/nginx/sites-available/hermes-tailscale.conf
server {
    listen $TS_IP:$PORT;
    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
# 安裝：
#   sudo cp hermes-tailscale.conf /etc/nginx/sites-available/
#   sudo ln -s /etc/nginx/sites-available/hermes-tailscale.conf /etc/nginx/sites-enabled/
#   sudo nginx -t && sudo systemctl reload nginx
EOF
exit 1
