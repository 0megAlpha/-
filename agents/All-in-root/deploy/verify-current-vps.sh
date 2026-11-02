#!/usr/bin/env bash
# Read-only smoke checks for the currently deployed greencloud-ai layout.
set -Eeuo pipefail
ROOT="${AGENT_SKILL_ROOT:-$HOME/AI-Agent-Skill}"
pass=0
fail=0
check_unit() {
  local unit="$1"
  if systemctl is-active --quiet "$unit"; then
    echo "PASS unit $unit"
    pass=$((pass+1))
  else
    echo "FAIL unit $unit"
    fail=$((fail+1))
  fi
}
check_http() {
  local name="$1" url="$2" expected="${3:-200}"
  local code
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 4 "$url" 2>/dev/null || true)"
  if [[ "$code" == "$expected" ]]; then
    echo "PASS http $name status=$code"
    pass=$((pass+1))
  else
    echo "FAIL http $name status=${code:-000} expected=$expected"
    fail=$((fail+1))
  fi
}
for unit in litellm.service openhands-litellm-bridge.service hermes-api.service dsh-agent.service agent-docker-port-guard.service; do
  check_unit "$unit"
done
check_http "LiteLLM readiness" "http://127.0.0.1:4000/health/readiness"
check_http "OpenHands local UI" "http://127.0.0.1:3000/"
check_http "Qdrant health" "http://127.0.0.1:6333/healthz"
if [[ -d "$ROOT/skills" ]]; then
  skill_count="$(find "$ROOT/skills" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | wc -l)"
  echo "INFO canonical skill definitions=$skill_count"
  [[ "$skill_count" -ge 20 ]] && pass=$((pass+1)) || { echo "FAIL expected at least 20 canonical skills"; fail=$((fail+1)); }
else
  echo "FAIL canonical skill root missing: $ROOT/skills"
  fail=$((fail+1))
fi
echo "INFO disk usage: $(df -h / | awk 'NR==2 {print $5 " used, " $4 " available"}')"
echo "INFO inference_e2e=NOT_CHECKED (provider inference can incur usage charges; model-catalog checks are not inference proof)"
echo "=== SUMMARY: $pass PASS / $fail FAIL ==="
(( fail == 0 ))
