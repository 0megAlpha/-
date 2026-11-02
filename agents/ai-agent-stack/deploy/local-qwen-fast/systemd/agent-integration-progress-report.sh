#!/usr/bin/env bash
set -eu
umask 077
state_dir=/var/lib/agent-integration
install -d -m 700 "$state_dir" "$state_dir/codex-home"
out="$state_dir/progress-latest.md"
tmp=$(mktemp "$state_dir/progress.XXXXXX")
trap 'rm -f "$tmp"' EXIT
{
  printf '# VPS Agent Integration Progress\n\n'
  printf -- '- Snapshot: `%s`\n' "$(date -Is)"
  printf -- '- Host: `%s`\n\n' "$(hostname)"
  printf '| Area | Snapshot |\n|---|---|\n'
  printf '| Disk `/` | `%s` |\n' "$(df -h / | awk 'NR==2 {print $3 " used / " $4 " free (" $5 ")"}')"
  codex_version=$(node -p "require('/usr/lib/node_modules/@openai/codex/package.json').version" 2>/dev/null || echo unknown)
  codex_auth=$(codex login status 2>&1 | grep -E "^(Not logged in|Logged in)" | tail -1 || true)
  if [[ -z "$codex_auth" ]]; then codex_auth=status-unavailable; fi
  printf '| Codex CLI | `%s`; `%s` |\n' "$codex_version" "$codex_auth"
  printf '| Claude Code | `%s` |\n' "$(claude --version 2>&1 | head -1)"
  printf '| OpenCode | `%s` |\n' "$(opencode --version 2>&1 | head -1)"
  for svc in litellm.service llama-agent-fast.service llama-agent.service openhands-litellm-bridge.service hermes-api.service hermes-gateway.service lody-agent.service dsh-agent.service; do
    printf '| systemd `%s` | `%s` |\n' "$svc" "$(systemctl is-active "$svc" 2>/dev/null || true)"
  done
  for pair in 'LiteLLM http://127.0.0.1:4000/health/readiness' 'Qwen-fast http://127.0.0.1:8089/health' 'OpenHands-bridge http://10.0.0.1:4001/health/readiness'; do
    label=${pair%% *}; url=${pair#* }
    code=$(curl -sS --max-time 2 -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || true)
    printf '| HTTP `%s` | `%s` |\n' "$label" "${code:-unreachable}"
  done
  printf '\n## Git worktrees\n\n| Repository | Branch/Tracking | Uncommitted paths | HEAD |\n|---|---|---:|---|\n'
  for r in /root/AI-Agent-Skill /root/ai-agent-stack /root/hermes-007 /root/ai-company /root/.hermes /root/open-hands; do
    if git -C "$r" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      branch=$(git -C "$r" status --short --branch | head -1 | sed 's/|/\\|/g')
      dirty=$(git -C "$r" status --short | wc -l | tr -d ' ')
      head=$(git -C "$r" log -1 --format='%h %cs %s' | sed 's/|/\\|/g')
      printf '| `%s` | `%s` | %s | `%s` |\n' "$r" "$branch" "$dirty" "$head"
    fi
  done
  printf '\n## Guardrails\n\n- Snapshot only; does not install, delete, restart, commit, or push anything.\n- GitHub PR checks and hosted SaaS deployments must be verified in their respective services.\n'
} > "$tmp"
chmod 600 "$tmp"
mv -f "$tmp" "$out"
