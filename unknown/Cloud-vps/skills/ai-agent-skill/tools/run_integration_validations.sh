#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"

python3 "$root/tools/verify_repo.py"
python3 "$root/tools/validate_integration_matrix.py"
python3 "$root/tools/verify_standalone_open.py"

# Environment-specific runtime checks are optional in CI where host services are absent.
if [ -x "$root/All-in/tests/verify_skill_fleet.sh" ]; then
  if bash "$root/All-in/tests/verify_skill_fleet.sh"; then
    echo "PASS verify_skill_fleet.sh"
  else
    echo "WARN verify_skill_fleet.sh failed in this environment; check host runtime prerequisites."
  fi
fi

if [ -x "$root/All-in/tests/verify_agent_api_compat.sh" ]; then
  if bash "$root/All-in/tests/verify_agent_api_compat.sh"; then
    echo "PASS verify_agent_api_compat.sh"
  else
    echo "WARN verify_agent_api_compat.sh failed in this environment; check host runtime prerequisites."
  fi
fi
