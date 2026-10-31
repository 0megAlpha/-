# VPS mirror inventory

Status date: 2026-11-01  
Source host: `agent-vps` (Ubuntu 26.04; SSH account `xiaye`)  
Target: `0megAlpha/-` — verified **private**, default branch `main`.  
This branch is an inventory checkpoint only. It does not claim that source repositories have been mirrored.

## Scope and mapping candidates

| VPS path | Suggested repository folder | Observed state | Notes / blockers |
|---|---|---|---|
| `/home/xiaye/Ai-agent-skill` | `Ai-agent-skill/` | branch `main`, ahead 1 / behind 24; tracked modification `push.sh`; untracked `FINAL_ENTRY.md`, `deploy/`, `fleet/`, `frontend/memory-viewer/`, workflow YAMLs | Priority Agent/skills collection. README previously found to contain merge-conflict markers. Needs content review and secrets scan before snapshot. |
| `/home/xiaye/repository/Google-AI` | `Google-AI/` | repository root exists, approx. 516 MB; staged gitlink/deletion changes were observed earlier | Contains `openhands-core/`, `openhands-cloud/`, `build-your-own-x-ref/` and nested/submodule content. Must preserve submodule ownership and pin metadata; exact recursive status not yet fully audited. |
| `/home/xiaye/hermes-007` | `hermes/` | branch `master`, behind 22; two untracked website secrets-related directories | Map as requested. Upstream is NousResearch/hermes-agent; preserve local fork origin and upstream distinction. Untracked secrets directories require review and must not be copied blindly. |
| `/home/xiaye/openhands-extensions` | `openhands-extensions/` | branch `main`, behind 86; clean worktree at initial status check | Public upstream clone. Keep distinct from integrated OpenHands runtime below. |
| `/opt/open-hands-integrated-main` | `openhands-integrated/` | approx. 7.5 MB; nested `.git` metadata present | Integrated OpenHands workspace; separate from upstream release checkout. |
| `/opt/openhands-upstream-build-v1.25.0` | `openhands-upstream-build-v1.25.0/` | detached HEAD at release commit `50c68a1`; approx. 33 MB | Preserve release snapshot separately; do not move detached HEAD or rewrite its origin. |
| `/home/xiaye/Claude-code` | `Claude-code/` | branch `main`, clean, tracks `origin/main` | AgentSys project; local origin is xh09411-web/Claude-code. |
| `/home/xiaye/All-in` | `All-in/` | branch `main`, behind 27; modified README/orchestrator/deploy/docker-compose; untracked `.env` and other files | Root-owned. `.env` explicitly excluded from any public or repository snapshot; inspect changes and example/template separately. |
| `/home/xiaye/CKA-Agent` | `CKA-Agent/` | branch `main`; modified `config/config.yml`, untracked backup; approx. 4.9 GB directory | Preserve user config and backup locally. Exclude virtualenv, datasets, experiment outputs and model artefacts unless individually approved. |
| `/opt/agent-plane` | `agent-plane/` | branch `master`; modified Caddyfile/Compose; untracked audit report, backups and dashboard files | Root-owned. Contains `secrets.env` and backups; exclude secret-bearing files and inspect config diffs before snapshot. |
| `/opt/sentinelx-cloud-core` | `sentinelx-cloud-core/` | branch `main`, clean tracked tree; untracked `.local/` and venv backup | Separate service/agent codebase; exclude runtime local data and virtualenv backups. |
| `/opt/sentinelx-python` | `sentinelx-python/` | approx. 103 MB; appears to include a Python runtime tree | Determine whether this is source or runtime distribution before mirroring; do not copy interpreter/site-packages blindly. |
| `/opt/hermes-agent-v0.22.5` | `hermes-agent-v0.22.5/` | approx. 609 MB; source checkout candidate | Separate installed Hermes source/version from `hermes-007`; repo metadata/remotes/status not yet verified. |
| `/opt/llama.cpp` | `llama.cpp/` | branch `master`; many tracked deletions under `models/`; approx. 293 MB | Upstream third-party runtime, not an Agent project. Preserve deletion state separately; exclude build products, model binaries and caches. |
| `/opt/openwebui-plugins` | `openwebui-plugins/` | approx. 24 KB | Local plugin/tool code; Git metadata not confirmed. |
| `/home/xiaye/ai-agent-fleet` | `ai-agent-fleet/` | approx. 1.1 GB | Agent fleet workspace; Git metadata and runtime/data boundaries not yet verified. |
| `/home/xiaye/freebuff-project` | `freebuff-project/` | approx. 852 KB | Project candidate; purpose and Git state not yet verified. |
| `/opt/agent-throne-file-center` | `agent-throne-file-center/` | approx. 12 KB | Local service/tool candidate; Git metadata not confirmed. |
| `/opt/dsh-sandbox` | `dsh-sandbox/` | approx. 20 KB | Sandbox/integration candidate; classify before mirroring. |
| `/opt/free-api` | `free-api/` | approx. 28 KB | Service candidate; classify before mirroring. |
| `/opt/agent-sandbox` | `agent-sandbox/` | approx. 20 KB | Sandbox candidate; classify before mirroring. |
| `/home/xiaye/.hermes/skills` | `agent-skills/hermes-user-skills/` | user-level skill location | Must inventory individual skill directories; do not copy runtime credentials/config from `.hermes`. |
| `/home/xiaye/Ai-agent-skill/agents`, `skills`, `plugins`, `workflows` | `Ai-agent-skill/` subfolders | collection includes multi-agent and skill/plugin catalogues | Preserve agent definitions, collaboration workflows, manifests and provenance. |

## Explicit exclusions / review gates

- Never mirror `.env`, `secrets.env`, private keys, access tokens, credential stores, SSH material, live databases, session state, logs containing secrets, or secrets directories without a separate safe export decision.
- Exclude `.git` internals from a folder snapshot only when the source Git history is preserved independently as a Git bundle or remote mirror. Do not silently discard history.
- Exclude virtual environments, `node_modules`, caches, build outputs, model weights, compiled binaries, datasets and experiment results by default. Keep a separate manifest of excluded artefacts and their sizes.
- Preserve all pre-existing staged/unstaged/untracked states. Do not reset, checkout over, clean, rebase, or fast-forward a dirty worktree.
- Do not update system packages or project dependencies until each project has an explicit lockfile/build/test plan and a backup of the current state.
- Third-party upstream repositories should be recorded as upstream references, not copied as if they were original user-authored projects. License and attribution files must be retained.

## Current blockers

1. VPS `gh` CLI is not authenticated.
2. VPS SSH does not yet trust GitHub's host key (strict host-key checking failed); no SSH push was attempted.
3. Gateway sudo is not configured, so root-owned directories and root-only files cannot be comprehensively inspected as the `xiaye` account.
4. The Gateway-managed SSH key and the user's Termius key are host-login keys; neither has been verified as a GitHub deploy key.
5. Full content transfer and history preservation have not yet been performed. This checkpoint is an inventory record, not a completed mirror.

## Next sync sequence

1. Complete root-owned and nested/submodule inventory with least-privilege read access.
2. Resolve project ownership, exact destination names, licenses, and runtime/data exclusions.
3. Create per-project snapshots preserving original Git history (Git bundle or branch/ref mirror) plus a readable folder layout.
4. Scan all candidate files for credentials and large binary/runtime artefacts.
5. Transfer each approved project into this private repository on its own branch/folder; verify file counts, hashes, commit ancestry and tree contents.
6. Fetch upstream updates separately and only fast-forward clean projects after local modifications are preserved.
7. Record validation/test results and any project that cannot be run due to missing secrets, services or dependencies.
