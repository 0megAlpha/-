#!/usr/bin/env bash
set -euo pipefail
MANIFEST="$1"
[ -n "$MANIFEST" ] || MANIFEST="$(dirname "$0")/../docs/PORTABLE_REPO_MANIFEST.tsv"
DEST="$2"
[ -n "$DEST" ] || DEST="./agent-repos"
OWNER="$(printenv GITHUB_OWNER || true)"
[ -n "$OWNER" ] || OWNER="tpisces88690"
command -v git >/dev/null || { echo "git is required" >&2; exit 2; }
mkdir -p "$DEST"
if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then gh auth setup-git >/dev/null 2>&1 || true; fi
ok=0; skipped=0; failed=0
while IFS="$(printf '\t')" read -r repo branch expected; do
  [ -z "$repo" ] && continue
  case "$repo" in \#*) continue ;; esac
  safe_branch="$(printf '%s' "$branch" | sed 's#/#__#g')"
  target="$DEST/$repo--$safe_branch"
  url="https://github.com/$OWNER/$repo.git"
  if [ -e "$target" ]; then
    if [ -d "$target/.git" ] && [ "$(git -C "$target" branch --show-current)" = "$branch" ]; then
      if [ -z "$(git -C "$target" status --porcelain)" ]; then
        if git -C "$target" fetch origin "$branch" >/dev/null 2>&1 && git -C "$target" merge --ff-only FETCH_HEAD >/dev/null 2>&1; then
          echo "UPDATED_FAST_FORWARD $repo $branch $(git -C "$target" rev-parse HEAD)"
          ok=$((ok+1))
        else
          echo "UPDATE_NEEDS_REVIEW $repo $branch"
          failed=$((failed+1))
        fi
      else
        echo "SKIP_DIRTY_PRESERVED $repo $branch -> $target"
        skipped=$((skipped+1))
      fi
    else
      echo "SKIP_EXISTS $repo $branch -> $target"
      skipped=$((skipped+1))
    fi
    continue
  fi
  if git ls-remote --exit-code "$url" "refs/heads/$branch" >/dev/null 2>&1; then
    if git clone --filter=blob:none --single-branch --branch "$branch" "$url" "$target"; then
      actual="$(git -C "$target" rev-parse HEAD)"
      if [ "$expected" = "-" ]; then
        echo "PULLED_LATEST $repo $branch $actual"
      else
        case "$actual" in "$expected"*) echo "PULLED_VERIFIED $repo $branch $actual" ;; *) echo "PULLED_SHA_CHANGED $repo $branch expected=$expected actual=$actual" ;; esac
      fi
      ok=$((ok+1))
    else
      echo "CLONE_FAILED $repo $branch"
      failed=$((failed+1))
    fi
  else
    echo "BRANCH_UNAVAILABLE $repo $branch"
    failed=$((failed+1))
  fi
done < "$MANIFEST"
printf 'SUMMARY pulled=%d skipped=%d failed=%d\n' "$ok" "$skipped" "$failed"
[ "$failed" -eq 0 ]
