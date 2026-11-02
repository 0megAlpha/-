#!/bin/bash
echo "=== Agent 獨立沙盒驗證 ==="
for n in openhands dsh opencode hermes; do
  if docker image inspect ${n}-sandbox:latest >/dev/null 2>&1; then
    echo "✅ ${n}-sandbox:latest 存在"
  else
    echo "❌ ${n}-sandbox:latest 缺失"
  fi
done
docker run --rm openhands-sandbox:latest python -c "print('py-ok')" 2>/dev/null && echo "✅ OpenHands 沙盒 Python 正常" || echo "⚠️ OpenHands 沙盒未就緒"
docker run --rm opencode-sandbox:latest node -e "console.log('js-ok')" 2>/dev/null && echo "✅ OpenCode 沙盒 Node 正常" || echo "⚠️ OpenCode 沙盒未就緒"
for f in /root/.openhands/config.toml /root/.openhands/skills/sandbox-testing.md /root/.dsh/cordis-sandbox.yml /root/.dsh/plugins/safe-code-execution.yml /root/.opencode/config.json /root/.opencode/plugins/sandbox-runner.js /opt/openwebui-plugins/tools/sub_agent.py /opt/openwebui-plugins/tools/parallel_tools.py /opt/openwebui-plugins/filters/vision_bridge.py /opt/redteam/tools/pyrit_config.py /opt/redteam/tools/garak_config.yaml /opt/redteam/prompts/injection_templates.json /opt/free-api/router.py; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f"
done
HM=/opt/army/hermes-agent; [ -d "$HM" ] || HM=/root/.hermes-sandbox-conf
[ -f "$HM/.env.sandbox" ] && echo "✅ $HM/.env.sandbox" || echo "❌ hermes sandbox env"
echo "=== 驗證結束 ==="
