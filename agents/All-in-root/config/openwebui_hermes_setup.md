# Open WebUI 連接 Hermes 指南

## 設定 → 連線 → OpenAI API
- API URL: http://host.docker.internal:8642/v1
- API Key: HERMES_API_KEY（由 docker-compose.yml 從 .env 注入，勿手動填真實值進設定檔）

## 模型選擇
- 選擇 hermes-agent

## 備註
- Open WebUI 容器需 `extra_hosts: host.docker.internal:host-gateway` 才能連到宿主機 8642
- 若 Hermes 只綁 127.0.0.1，容器內無法連線 → 跑 deploy/fix/01 修復綁定
