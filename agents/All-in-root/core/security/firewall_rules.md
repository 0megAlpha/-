# 防火牆與暴露面政策（All-in）

> 原則：**內部服務永遠不對公網暴露**。0.0.0.0 綁定只是「讓 Tailscale 介面能連上」，
> 公網閘道必須由防火牆擋死。

## ufw（Ubuntu 建議）

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow in on tailscale0            # 只信任 Tailscale 介面
# 或更嚴格：只放行 Tailscale 網段（100.64.0.0/10 是 CGNAT/Tailscale 保留段）
for port in 8642 6333 3000 8000 18000 8743 4000 5678; do
  sudo ufw allow from 100.64.0.0/10 to any port $port proto tcp comment 'tailscale-only'
done
sudo ufw enable
sudo ufw status verbose
```

## 端口政策
| 端口 | 服務 | 暴露等級 |
|---|---|---|
| 8642 | Hermes | 僅 Tailscale（dashboard/手機端用） |
| 6333/6334 | Qdrant | 僅 Tailscale；公網暴露等於把記憶庫送人 |
| 3000 | Open WebUI | 僅 Tailscale |
| 8000 | Mem0 | 僅 Tailscale |
| 18000/8743/4000/5678 | OpenHands/OpenCode/LiteLLM/n8n | 僅 Tailscale |
| 11434 | Ollama | **僅 127.0.0.1**（不得綁 0.0.0.0） |

## Hermes 反向代理備案（fix/01 用）
```nginx
# /etc/nginx/sites-available/hermes-tailscale.conf
server {
    listen 100.126.48.60:8642;
    location / {
        proxy_pass http://127.0.0.1:8642;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
# sudo ln -s ../sites-available/hermes-tailscale.conf /etc/nginx/sites-enabled/
# sudo nginx -t && sudo systemctl reload nginx
```

## 跨網域（CORS）
監控面板（all-in-dashboard / collaboration-monitor）以瀏覽器 fetch Hermes/Qdrant，
Hermes 端需允許來自面板 origin 的 `Access-Control-Allow-Origin`，否則面板會顯示 offline。
