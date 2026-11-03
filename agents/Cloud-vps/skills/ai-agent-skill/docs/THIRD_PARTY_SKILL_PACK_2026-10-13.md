# Third-party Skill Pack — 2026-10-13

This pack vendors selected third-party skills into the private `Ai-Agent-Skill` repository so the shared capability layer can be versioned and reviewed. It does not copy provider credentials, personal settings, workspace state, or agent memory.

## Included sources

| Local path | Upstream source | Intended use |
|---|---|---|
| `skills/third-party/git-guardrails-claude-code/` | [`mattpocock/skills`](https://github.com/mattpocock/skills) | MIT; safer Git operations in Claude Code |
| `skills/third-party/agent-browser/` | [`vercel-labs/agent-browser`](https://github.com/vercel-labs/agent-browser) | Apache-2.0; browser automation workflows |
| `skills/third-party/supabase-postgres-best-practices/` | [`supabase/agent-skills`](https://github.com/supabase/agent-skills) | MIT; PostgreSQL / Supabase design and query practices |
| `skills/third-party/prisma-client-api/` | [`prisma/skills`](https://github.com/prisma/skills) | MIT; Prisma Client usage |

## Installation and verification notes

- Installed shared copies are under `/root/.agents/skills/` on the VPS.
- Claude Code skill symlinks were verified to resolve to the shared copies.
- The skills CLI reports these skills as universal for Codex, Cline, and OpenCode; those agents still require a per-agent load check before being marked `VERIFIED`.
- Lody's `Claude Code` agent config currently has no explicit `env` values. A working end-to-end Lody task is not yet verified because the active provider/model route has timed out and the configured NVIDIA/DeepSeek key values contain non-ASCII characters.
- The Vercel React / React Native / composition skills are installed locally, but are not vendored here because a root license file could not be verified during this pass.
- UI/UX Pro Max is installed locally, but its multi-megabyte catalog and fixture bundle is not vendored to keep the shared repository lean.
- Anthropic PDF and PPTX skills are installed locally, but are not vendored here because their `LICENSE.txt` places use under the user's agreement with Anthropic services rather than a general redistribution license.
- This pack is a versioned source copy, not proof that every runtime has loaded or successfully executed every skill. Review upstream licenses and update provenance when syncing newer versions.
