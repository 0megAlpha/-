#!/usr/bin/env bash
set -euo pipefail
ROOT=/root/AI-Agent-Skill
for d in /root/.agents/skills /root/.claude/skills /root/.config/opencode/skills /root/.hermes/skills /root/.openhands/skills /root/.dsh/skills /root/.cline/skills; do
  test -d "$d" || { echo "FAIL missing target $d"; exit 1; }
done
for s in engineering-memory define-to-ship plan-once-verify-always agent-skills ecc vps-bridge apollo-memory sesm-engine harness-evolution obra-superpowers firecrawl composio understand-anything skill-optimizer api-compatibility agent-fleet-secure-workflow full-cycle-mobile-dev agentic-security-review; do
  test -s "$ROOT/skills/$s/SKILL.md" || { echo "FAIL missing source skill $s"; exit 1; }
  for d in /root/.agents/skills /root/.claude/skills /root/.config/opencode/skills /root/.hermes/skills /root/.openhands/skills /root/.dsh/skills /root/.cline/skills; do
    test -s "$d/$s/SKILL.md" || { echo "FAIL missing installed skill $d/$s"; exit 1; }
  done
done
python3 -m py_compile "$ROOT/All-in/orchestrator/langgraph_workflow.py"
python3 - <<'PY2'
import json
p='/root/AI-Agent-Skill/integrations/agent-registry/skill-fleet.generated.json'
d=json.load(open(p))
assert len(d['skills']) >= 13, len(d.get('skills', []))
assert len(d['agents']) == 7, len(d.get('agents', {}))
print('PASS manifest JSON; skills:', len(d['skills']), 'agent targets:', len(d['agents']))
PY2
echo "PASS skill source, all seven agent target directories, and Python syntax"
if python3 -c 'import langgraph' 2>/dev/null; then echo 'PASS LangGraph import available'; else echo 'BLOCKED LangGraph package not installed; workflow source prepared, runtime not enabled'; fi
