#!/bin/bash
# 租用 VPS 遷移逃生艙 v2
set -e
git clone git@github.com:xh09411-web/Ai-Agent-Skill.git ~/Ai-Agent-Skill-repo
git clone git@github.com:xh09411-web/hermes-007.git ~/.hermes
git clone git@github.com:xh09411-web/open-hands.git ~/open-hands-workspace
git clone git@github.com:xh09411-web/ai-agent-stack.git ~/ai-agent-stack
sudo apt-get update && sudo apt-get install -y docker.io nginx redis-server tailscale npm python3-pip git
[ -f ~/.hermes/requirements.txt ] && sudo pip install --break-system-packages -r ~/.hermes/requirements.txt || true
sudo pip install --break-system-packages litellm
[ -f ~/.hermes/npm-global.list ] && npm i -g $(grep -oE '[@A-Za-z0-9/._-]+@[0-9]+[^ ]*' ~/.hermes/npm-global.list | tr '\n' ' ') || true
mkdir -p ~/.openhands/skills && cp -r ~/open-hands-workspace/extensions-custom/* ~/.openhands/skills/ 2>/dev/null || true
echo "✅ 還原完成；systemd/容器依 ~/ai-agent-stack/portable/vps-export/manifests/ 恢復"
