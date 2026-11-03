#!/bin/bash
set -e

echo "=== Hermes Agent + OpenHands 一鍵部署 ==="
cd ~/hermes-007
export PATH="$HOME/.local/bin:$PATH"

# 1. 啟動虛擬環境
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✓ 虛擬環境已載入"
else
    echo "✗ 虛擬環境不存在，先執行安裝..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv sync --all-extras
    source .venv/bin/activate
fi

# 2. 啟動 OpenHands（如果沒跑）
if ! docker ps | grep -q openhands; then
    docker rm -f openhands 2>/dev/null || true
    docker run -d --name openhands \
        -p 3000:3000 \
        -v /var/run/docker.sock:/var/run/docker.sock \
        ghcr.io/opendevin/opendevin:main
    echo "✓ OpenHands 已啟動 http://你的VPS_IP:3000"
else
    echo "✓ OpenHands 已在運行"
fi

# 3. 啟動 Hermes Agent 背景 Session
if ! tmux ls 2>/dev/null | grep -q hermes-agent; then
    tmux new-session -d -s hermes-agent "cd ~/hermes-007 && source .venv/bin/activate && bash"
    echo "✓ Hermes Agent 背景 Session 已建立"
else
    echo "✓ Hermes Agent 背景 Session 已在運行"
fi

# 4. 自動推送到 GitHub（保存長期記憶）
if [ -d ".git" ]; then
    git add -A 2>/dev/null || true
    git commit -m "Auto update $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null || true
    git push origin master 2>/dev/null || true
    echo "✓ GitHub 已同步"
fi

# 5. 清理垃圾
rm -rf ~/.cache/pip /tmp/pip-* 2>/dev/null
docker system prune -f 2>/dev/null || true

# 6. 狀態報告
echo ""
echo "=== 所有服務狀態 ==="
echo "Hermes Agent: tmux attach -t hermes-agent"
echo "OpenHands:    http://你的VPS_IP:3000"
echo "AnythingLLM:  http://你的VPS_IP:3001"
echo "LiteLLM:      http://你的VPS_IP:4000"
echo "GitHub:       https://github.com/xh09411-web/hermes-007"
echo ""
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "=== 完成 ==="
echo "iPhone 可以關閉 App，所有服務在 VPS 背景繼續跑"
