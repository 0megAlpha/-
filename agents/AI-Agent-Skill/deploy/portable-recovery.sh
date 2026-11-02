#!/usr/bin/env bash
# Portable recovery helper. Default is a safe plan; --apply copies only missing SKILL.md files.
set -Eeuo pipefail
REPO_URL="${AGENT_SKILL_REPO_URL:-https://github.com/xh09411-web/Ai-Agent-Skill.git}"
DEST="${AGENT_SKILL_REPO_DIR:-$HOME/AI-Agent-Skill}"
APPLY=0
for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    -h|--help)
      echo "Usage: $0 [--apply]"
      echo "Default: clone/fetch the canonical repository and validate it without modifying agent skill roots."
      echo "--apply: copy missing skill definitions; existing skill directories are never overwritten."
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done
command -v git >/dev/null || { echo "ERROR: git is required" >&2; exit 1; }
if [[ -d "$DEST/.git" ]]; then
  echo "Existing repository: $DEST"
  git -C "$DEST" fetch --prune origin
  echo "Fetched origin; local worktree was not reset or overwritten."
else
  if [[ -e "$DEST" ]]; then
    echo "ERROR: destination exists but is not a Git repository: $DEST" >&2
    exit 1
  fi
  git clone --filter=blob:none "$REPO_URL" "$DEST"
fi
python3 "$DEST/tools/verify_repo.py"
mapfile -t SKILL_FILES < <(find "$DEST/skills" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)
TARGETS=()
for d in "$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.config/opencode/skills" "$HOME/.hermes/skills" "$HOME/.openhands/skills" "$HOME/.dsh/skills" "$HOME/.cline/skills"; do
  [[ -d "$d" ]] && TARGETS+=("$d")
done
echo "Canonical repo: $DEST"
echo "Skill definitions: ${#SKILL_FILES[@]}"
echo "Detected existing agent skill roots: ${#TARGETS[@]}"
if (( ! APPLY )); then
  echo "DRY RUN: no agent files changed. Re-run with --apply after reviewing this plan."
  exit 0
fi
for target in "${TARGETS[@]}"; do
  for src in "${SKILL_FILES[@]}"; do
    skill="$(basename "$(dirname "$src")")"
    dst="$target/$skill"
    if [[ -e "$dst" ]]; then
      continue
    fi
    mkdir -p "$dst"
    cp -n "$src" "$dst/SKILL.md"
  done
done
echo "PASS: missing skill definitions copied; existing skills were preserved."
