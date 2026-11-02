#!/usr/bin/env bash
# Safe recovery of the user's canonical private agent repositories.
# Default is a dry run. --apply clones missing repositories and fast-forwards only clean worktrees.
set -Eeuo pipefail
APPLY=0
for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    -h|--help)
      echo "Usage: bash restore/restore-vps-safe.sh [--apply]"
      echo "Default: print the recovery plan. --apply performs clone/fast-forward only on clean worktrees."
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

# Format: GitHub repository name | branch | local checkout directory.
repos=(
  "Ai-Agent-Skill|main|AI-Agent-Skill"
  "All-in|main|All-in"
  "ai-agent-stack|portable-20260924|ai-agent-stack"
  "ai-agent-fleet|main|ai-agent-fleet"
)
root="${AGENT_RECOVERY_ROOT:-$HOME}"
for item in "${repos[@]}"; do
  repo="${item%%|*}"
  rest="${item#*|}"
  branch="${rest%%|*}"
  dest_name="${rest##*|}"
  dest="$root/$dest_name"
  url="https://github.com/xh09411-web/$repo.git"
  if [[ -d "$dest/.git" ]]; then
    if [[ -n "$(git -C "$dest" status --porcelain)" ]]; then
      echo "PRESERVE_DIRTY $dest (no fetch, checkout, reset, or overwrite)"
      continue
    fi
    current="$(git -C "$dest" branch --show-current)"
    if [[ "$current" != "$branch" ]]; then
      echo "SKIP_BRANCH_MISMATCH $dest current=$current expected=$branch"
      continue
    fi
    echo "UPDATE_CLEAN $dest branch=$branch"
    if (( APPLY )); then
      git -C "$dest" fetch origin "$branch"
      git -C "$dest" merge-base --is-ancestor HEAD "origin/$branch"
      git -C "$dest" merge --ff-only "origin/$branch"
    fi
  elif [[ -e "$dest" ]]; then
    echo "SKIP_NON_GIT_PATH $dest (preserved)"
  else
    echo "CLONE_MISSING $url -> $dest branch=$branch"
    if (( APPLY )); then
      git clone --filter=blob:none --branch "$branch" "$url" "$dest"
    fi
  fi
done
if (( ! APPLY )); then
  echo "DRY_RUN_ONLY: no files or services changed. Use --apply after reviewing the plan."
else
  echo "PASS: repository recovery completed without force-push, hard reset, service start, or secret creation."
fi
