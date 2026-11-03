---
name: vps-bridge
description: SSH 遠端執行、部署、檔案同步、Docker 管理（僅限自有基礎設施）。
version: "1.0.0"
owner: "All-in"
---
# 安全規則（硬性）
- 禁止 rm -rf /、mkfs.*、dd if=/dev/zero 等毀滅性命令
- 生產環境操作前必須二次確認（human approval）
- 修改配置前自動備份（.bak.時間戳）
- 所有操作記錄到 ~/.hermes/logs/vps-bridge.log

# 能力
ssh exec ／ scp ／ rsync ／ docker-remote ／ tmux 保活 ／ port-forward
