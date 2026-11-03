#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
root="${AI_AGENT_SKILL_ROOT:-$(cd "$script_dir/.." && pwd)}"

# Optional private overrides (ignored by git) for runtime remotes/branches.
if [ -f "$script_dir/load-local-overlay.sh" ]; then
  # shellcheck disable=SC1091
  . "$script_dir/load-local-overlay.sh"
fi

# Bootstrap only source code. Never copies credentials, memory or private workspace state.
clone(){ local name="$1" url="$2" branch="$3"; if [ ! -d "$root/$name/source/.git" ]; then git clone --filter=blob:none --branch "$branch" "$url" "$root/$name/source"; else git -C "$root/$name/source" fetch --prune origin; fi; }
clone claude-code "${RUNTIME_CLAUDE_CODE_REMOTE:-git@github.com:xh09411-web/Claude-code.git}" "${RUNTIME_CLAUDE_CODE_BRANCH:-main}"
clone opencode "${RUNTIME_OPENCODE_REMOTE:-git@github.com:anomalyco/opencode.git}" "${RUNTIME_OPENCODE_BRANCH:-dev}"
clone dsh "${RUNTIME_DSH_REMOTE:-git@github.com:xh09411-web/--dsh.git}" "${RUNTIME_DSH_BRANCH:-main}"
clone cuga "${RUNTIME_CUGA_REMOTE:-git@github.com:xh09411-web/-cuga-agent-.git}" "${RUNTIME_CUGA_BRANCH:-main}"
clone pentestgpt "${RUNTIME_PENTESTGPT_REMOTE:-git@github.com:xh09411-web/-PentestGPT-.git}" "${RUNTIME_PENTESTGPT_BRANCH:-main}"
clone oh-my-agent "${RUNTIME_OH_MY_AGENT_REMOTE:-https://github.com/xh09411-web/-oh-my-agent-.git}" "${RUNTIME_OH_MY_AGENT_BRANCH:-main}"
clone flowise "${RUNTIME_FLOWISE_REMOTE:-git@github.com:xh09411-web/flowise-LLM.git}" "${RUNTIME_FLOWISE_BRANCH:-main}"
clone codex "${RUNTIME_CODEX_REMOTE:-https://github.com/openai/codex.git}" "${RUNTIME_CODEX_BRANCH:-main}"
