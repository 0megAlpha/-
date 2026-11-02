#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
SOURCE_SCRIPT="$ROOT/scripts/link-shared-skills.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OPEN="$TMP/open-hands"
SHARED="$TMP/Ai-Agent-Skill"
mkdir -p "$OPEN/scripts" "$OPEN/.agents/skills" "$SHARED/skills"
git -C "$OPEN" init -q
cp "$SOURCE_SCRIPT" "$OPEN/scripts/link-shared-skills.sh"
chmod +x "$OPEN/scripts/link-shared-skills.sh"
git -C "$SHARED" init -q
git -C "$SHARED" config user.name test
git -C "$SHARED" config user.email test@example.invalid
links=(
  'agent-skills|agent-skills'
  'apollo-memory|apollo-memory'
  'composio|composio'
  'composio-tool-integration|composio-tool-integration'
  'define-to-ship|define-to-ship'
  'ecc|ecc'
  'engineering-memory|engineering-memory'
  'evolution-tree/evolution-tree|evolution-tree'
  'firecrawl|firecrawl'
  'firecrawl-web-research|firecrawl-web-research'
  'full-cycle-mobile-dev|full-cycle-mobile-dev'
  'harness-evolution|harness-evolution'
  'obra-superpowers|obra-superpowers'
  'plan-once-verify-always|plan-once-verify-always'
  'recovered-from-freebuff|recovered-from-freebuff'
  'sesm-engine|sesm-engine'
  'skill-optimizer|skill-optimizer'
  'understand-anything|understand-anything'
  'vps-bridge|vps-bridge'
)
for entry in "${links[@]}"; do
  src="${entry#*|}"
  mkdir -p "$SHARED/skills/$src"
  printf '# fixture %s\n' "$src" > "$SHARED/skills/$src/SKILL.md"
done
git -C "$SHARED" add skills
git -C "$SHARED" commit -qm fixture
git -C "$SHARED" remote add origin https://github.com/xh09411-web/Ai-Agent-Skill.git
PIN="$(git -C "$SHARED" rev-parse HEAD)"
export AI_AGENT_SKILL_REPO="$SHARED" AI_AGENT_SKILL_COMMIT="$PIN" AI_AGENT_SKILL_URL=https://github.com/xh09411-web/Ai-Agent-Skill.git
"$OPEN/scripts/link-shared-skills.sh" --dry-run >/dev/null
if find "$OPEN/.agents/skills" -type l -print -quit | grep -q .; then echo 'FAIL: dry-run created symlinks' >&2; exit 1; fi
"$OPEN/scripts/link-shared-skills.sh" >/dev/null
for entry in "${links[@]}"; do
  dest="${entry%%|*}"
  src="${entry#*|}"
  test -L "$OPEN/.agents/skills/$dest"
  test "$(readlink -f "$OPEN/.agents/skills/$dest")" = "$SHARED/skills/$src"
done
rm "$OPEN/.agents/skills/firecrawl"
mkdir "$OPEN/.agents/skills/firecrawl"
printf 'keep me\n' > "$OPEN/.agents/skills/firecrawl/LOCAL.txt"
if "$OPEN/scripts/link-shared-skills.sh" >/dev/null 2>&1; then echo 'FAIL: conflict should have failed' >&2; exit 1; fi
test "$(cat "$OPEN/.agents/skills/firecrawl/LOCAL.txt")" = 'keep me'
echo 'PASS: dry-run, pinned-source links, and no-overwrite conflict checks'
