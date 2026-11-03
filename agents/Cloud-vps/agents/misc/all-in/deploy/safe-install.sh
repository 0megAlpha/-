#!/usr/bin/env bash
# Safe, non-destructive All-in skill synchronizer.
# Default is a dry run. --apply copies only missing SKILL.md files.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APPLY=0
for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    -h|--help)
      echo "Usage: bash deploy/safe-install.sh [--apply]"
      echo "Default: report a plan only; --apply copies missing skills and never overwrites existing files."
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

[[ -d "$ROOT/skills" ]] || { echo "ERROR: skills directory missing: $ROOT/skills" >&2; exit 1; }
TARGETS=()
for d in "$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.config/opencode/skills" "$HOME/.hermes/skills" "$HOME/.openhands/skills" "$HOME/.dsh/skills" "$HOME/.cline/skills"; do
  [[ -d "$d" ]] && TARGETS+=("$d")
done

count=0
while IFS= read -r -d '' src; do
  skill="$(basename "$(dirname "$src")")"
  for target in "${TARGETS[@]}"; do
    dst="$target/$skill/SKILL.md"
    if [[ -s "$dst" ]]; then
      continue
    fi
    count=$((count+1))
    if (( APPLY )); then
      mkdir -p "$target/$skill"
      install -m 0644 "$src" "$dst"
      echo "INSTALLED $dst"
    else
      echo "WOULD_INSTALL $dst"
    fi
  done
done < <(find "$ROOT/skills" -mindepth 2 -maxdepth 2 -type f -name SKILL.md -print0 | sort -z)

echo "Skill definitions: $(find "$ROOT/skills" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | wc -l)"
echo "Detected existing agent skill roots: ${#TARGETS[@]}"
echo "Missing skill files: $count"
if (( ! APPLY )); then
  echo "DRY_RUN_ONLY: no files changed; pass --apply to install missing files."
else
  echo "PASS: only missing skill files were added; existing files were preserved."
fi
