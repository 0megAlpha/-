#!/usr/bin/env bash
# Link shared skills from the canonical Ai-Agent-Skill repository without copying files.
set -euo pipefail

OPENHANDS_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
AI_AGENT_SKILL_URL="${AI_AGENT_SKILL_URL:-https://github.com/xh09411-web/Ai-Agent-Skill.git}"
AI_AGENT_SKILL_BRANCH="${AI_AGENT_SKILL_BRANCH:-fix/allow-absent-litellm-proxy-20261009}"
AI_AGENT_SKILL_COMMIT="${AI_AGENT_SKILL_COMMIT:-39112117be17b67b40944681e753ac9ed7dd5091}"
AI_AGENT_SKILL_REPO="${AI_AGENT_SKILL_REPO:-$(dirname "$OPENHANDS_ROOT")/AI-Agent-Skill}"
DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then DRY_RUN=1; elif [[ $# -gt 0 ]]; then echo "usage: $0 [--dry-run]" >&2; exit 2; fi

say() { printf '%s\n' "$*"; }
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

if [[ ! -d "$AI_AGENT_SKILL_REPO/.git" ]]; then
  if (( DRY_RUN )); then
    say "DRY RUN: would clone $AI_AGENT_SKILL_URL at $AI_AGENT_SKILL_COMMIT to $AI_AGENT_SKILL_REPO"
    exit 0
  fi
  [[ ! -e "$AI_AGENT_SKILL_REPO" ]] || fail "destination exists but is not a Git checkout: $AI_AGENT_SKILL_REPO"
  git clone --branch "$AI_AGENT_SKILL_BRANCH" --single-branch "$AI_AGENT_SKILL_URL" "$AI_AGENT_SKILL_REPO"
  git -C "$AI_AGENT_SKILL_REPO" checkout --detach "$AI_AGENT_SKILL_COMMIT"
fi

origin="$(git -C "$AI_AGENT_SKILL_REPO" remote get-url origin 2>/dev/null || true)"
case "$origin" in
  "$AI_AGENT_SKILL_URL"|git@github.com:xh09411-web/Ai-Agent-Skill.git) ;;
  *) fail "unexpected origin for shared skills checkout: $AI_AGENT_SKILL_REPO" ;;
esac
head="$(git -C "$AI_AGENT_SKILL_REPO" rev-parse HEAD 2>/dev/null || true)"
[[ "$head" == "$AI_AGENT_SKILL_COMMIT" ]] || fail "shared skills checkout must be at pinned commit $AI_AGENT_SKILL_COMMIT (found ${head:-none}); use a dedicated checkout or set AI_AGENT_SKILL_REPO"
[[ -z "$(git -C "$AI_AGENT_SKILL_REPO" status --porcelain 2>/dev/null)" ]] || fail "shared skills checkout has local changes; refusing to link mutable content"

# OpenHands-relative destination | path inside the canonical shared repository.
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
  rel_dest="${entry%%|*}"
  rel_src="${entry#*|}"
  src="$AI_AGENT_SKILL_REPO/skills/$rel_src"
  dest="$OPENHANDS_ROOT/.agents/skills/$rel_dest"
  [[ -d "$src" ]] || fail "missing shared skill source: $src"
  if [[ -L "$dest" ]]; then
    current="$(readlink -f "$dest" 2>/dev/null || true)"
    [[ "$current" == "$src" ]] || fail "existing symlink points elsewhere; refusing to replace: $dest"
    say "OK existing link: .agents/skills/$rel_dest"
  elif [[ -e "$dest" ]]; then
    fail "destination already exists and is not the expected symlink; refusing to overwrite: $dest"
  elif (( DRY_RUN )); then
    say "DRY RUN: link .agents/skills/$rel_dest -> $src"
  else
    mkdir -p "$(dirname "$dest")"
    relative_target="$(realpath --relative-to="$(dirname "$dest")" "$src")"
    ln -s "$relative_target" "$dest"
    say "LINKED .agents/skills/$rel_dest"
  fi
done
say "Shared skill link check complete at pinned commit $AI_AGENT_SKILL_COMMIT"
