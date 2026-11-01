# VPS Agent Inventory and Destination Map

Last checked: 2026-11-01  
Source: VPS `agent-vps` only. This file deliberately excludes agents or skills found only in external accounts or the wider web.

Target repository: `0megAlpha/-` (private)  
Working branch: `vps-mirror/inventory-2026-11`

## Confirmed Agent-related projects on the VPS

| VPS source | Intended destination folder | Current evidence | Transfer status |
|---|---|---|---|
| `/home/xiaye/Ai-agent-skill` | `Ai-agent-skill/` | 6,175 non-runtime files, about 65 MB; local `main` is ahead 1 / behind 24; local changes include `push.sh`, `FINAL_ENTRY.md`, `deploy/`, `fleet/`, `frontend/memory-viewer/`, and workflow YAMLs | Not mirrored yet. Root-owned; needs one-time sudo for Git operations. README contains unresolved merge-conflict markers and two conflicting architecture descriptions. |
| `/home/xiaye/repository/Google-AI` | `Google-AI/` | Approx. 516 MB. Includes `openhands-core/`, `openhands-cloud/`, `build-your-own-x-ref/`; earlier status showed staged gitlink/deletion changes | Not mirrored yet. Needs root-owned/submodule review and exact recursive mapping. |
| `/home/xiaye/hermes-007` | `hermes/` | Hermes Agent source; local `master` is behind `origin/master` by 22 commits; untracked secrets-related website directories exist | Not mirrored yet. Keep untracked secret-bearing paths out of the mirror. |
| `/opt/hermes-agent-v0.22.5` | `hermes-agent-v0.22.5/` | Installed/source snapshot, about 609 MB | Separate versioned copy; do not merge into `hermes/` until Git metadata and provenance are checked. |
| `/home/xiaye/openhands-extensions` | `openhands-extensions/` | Official OpenHands extensions registry; 82 extensions in the currently read README catalog | Upstream fast-forward was completed earlier; a later fetch refreshed tags but could not update all refs due ownership/permission on one ref. Re-verify before claiming fully current. |
| `/opt/open-hands-integrated-main` | `openhands-integrated/` | Integrated OpenHands workspace, about 7.5 MB, nested Git metadata | Not mirrored yet; keep separate from upstream extensions and release snapshots. |
| `/opt/openhands-upstream-build-v1.25.0` | `openhands-upstream-build-v1.25.0/` | OpenHands upstream release checkout, detached at commit `50c68a1`, about 33 MB | Not mirrored yet; preserve exact detached release snapshot. |
| `/home/xiaye/Claude-code` | `Claude-code/` | AgentSys source; 404 non-runtime files, about 4.2 MB; clean `main` at `18399889` | Not mirrored yet. Fetch failed because the VPS has no HTTPS GitHub credential; do not assume remote is current. |
| `/home/xiaye/ai-agent-fleet` | `ai-agent-fleet/` | Agent Fleet workspace, about 1.1 GB | Not mirrored yet; determine source/runtime/data boundaries before transfer. |
| `/opt/agent-plane` | `agent-plane/` | Agent deployment/control-plane project; local Caddy/Compose changes and untracked reports/dashboard files | Not mirrored yet. Root-owned; inspect local diffs and exclude secret-bearing files. |
| `/opt/sentinelx-cloud-core` | `sentinelx-cloud-core/` | SentinelX remote-agent/cloud control plane; tracked tree was clean, with untracked local runtime data | Not mirrored yet. Preserve runtime data locally; review code and deployment manifests separately. |
| `/opt/sentinelx-python` | `sentinelx-python/` | About 103 MB; may include Python runtime/site-packages | Classification required; do not copy interpreter or installed dependencies as source code. |
| `/home/xiaye/CKA-Agent` | `CKA-Agent/` | Kubernetes Agent/security research project; about 4.9 GB; local config modification and backup file | Not mirrored yet. Preserve local config and backup; exclude virtualenv, datasets, models and experiment output unless specifically classified as source. |
| `/home/xiaye/All-in` | `All-in/` | Agent orchestration project; modified README/orchestrator/deploy/Compose files; contains `.env` | Not mirrored yet. `.env` and other secret files are excluded. Root-owned. |
| `/opt/openwebui-plugins` | `openwebui-plugins/` | Small local plugin/tool collection | Not mirrored yet; inspect manifests and source. |
| `/home/xiaye/.hermes/skills` | `agent-skills/hermes-user-skills/` | User-level Hermes skills directory | Not mirrored yet; copy skill source only, not Hermes config, tokens, sessions or memory databases. |

## Agent-related directories found but not yet classified

These are VPS paths only. They do not yet have verified destination folders or enough inspected content to assign a reliable project identity. Keep them in this list until their purpose and contents are confirmed.

| VPS path | Proposed future folder | Current status |
|---|---|---|
| `/root/-oh-my-agent-/` | `oh-my-agent/` | Root-owned; contents and Git remotes not fully read. |
| `/root/-DARPA-AIxCC-/` | `DARPA-AIxCC/` | Root-owned; contents and Git remotes not fully read. |
| `/root/AI-Agent-Skill/` | `AI-Agent-Skill-root/` | Candidate directory; confirm whether duplicate, fork, or distinct project. |
| `/root/Ai-Agent-Skill-workspace/` | `Ai-Agent-Skill-workspace/` | Candidate directory; relationship to `/home/xiaye/Ai-agent-skill` unknown. |
| `/root/agents/` | `agents/` | Candidate Agent definitions; contents not reviewed. |
| `/root/agent-system/` | `agent-system/` | Candidate Agent framework; contents not reviewed. |
| `/root/agent-integration/` | `agent-integration/` | Candidate integration workspace; contents not reviewed. |
| `/root/ai-agent-stack/` | `ai-agent-stack/` | Candidate stack; contents not reviewed. |
| `/root/ai-agent-fleet/` | `ai-agent-fleet-root/` | Candidate duplicate of home Agent Fleet; compare before assigning. |
| `/root/hermes-repo/` | `hermes-repo/` | Candidate Hermes source; relation to other Hermes checkouts unknown. |
| `/root/hermes-ultimate/` | `hermes-ultimate/` | Candidate Hermes project; not reviewed. |
| `/root/open-hands/` | `open-hands-root/` | Candidate OpenHands checkout; relation to other OpenHands copies unknown. |
| `/root/openhands-extensions/` | `openhands-extensions-root/` | Candidate duplicate of the home extensions checkout; compare exact origin and HEAD first. |
| `/root/openhands-skill-backups/` | `openhands-skill-backups/` | Backup candidate; inspect before transfer. |
| `/root/ASTRA_Core/` | `ASTRA_Core/` | Candidate Agent/core project; not reviewed. |
| `/root/Ghost_Core/` | `Ghost_Core/` | Candidate Agent/core project; not reviewed. |
| `/root/REALM_Bridge/` | `REALM_Bridge/` | Candidate Agent integration/bridge; not reviewed. |
| `/root/projects/` and `/root/workspace/` | Not assigned | Potential nested projects; enumerate Git roots before creating folders. |

## Collaboration and multi-agent components to preserve

- `Ai-agent-skill/agents/`, `skills/`, `plugins/`, `workflows/`, and collaboration-monitor frontend are first-class source assets, not just documentation.
- `Claude-code` / AgentSys includes multi-agent orchestration, specialist agents, pipeline phase gates, PR/CI workflows, code review, and persistent state.
- `hermes-007` includes subagents, messaging gateway integrations, skills, memory and scheduled automation.
- OpenHands extensions are reusable Skills, Plugins and Canvas Apps; integrated runtime and upstream release snapshots remain separate.
- `agent-plane`, `sentinelx-cloud-core`, and `ai-agent-fleet` are deployment/control-plane or fleet components and should not be collapsed into a single generic Agent folder.
- Google-AI nested OpenHands projects need their own nested destination mapping after submodule metadata is inspected.

## Synchronization rules

1. Preserve original Git histories, branches, tags, remotes and submodule/gitlink metadata wherever possible. Do not flatten different repositories into one folder without preserving provenance.
2. Preserve every local modification, staged change, untracked source file and deletion. Never reset, clean, force-push, rebase or overwrite a dirty worktree.
3. Exclude credentials, `.env*`, `secrets.env`, tokens, private keys, SSH material, credential stores, session state, live databases, secret-bearing logs and runtime data.
4. Exclude virtualenvs, `node_modules`, build outputs, caches, model weights, datasets and compiled binaries by default; list excluded large artefacts separately.
5. For source repos with no matching destination directory, record them here and wait for the user-created folder rather than guessing.
6. A repo is only marked mirrored after file-tree and hash checks, commit/ref verification, and a clean Git status. A successful inventory or API metadata write is not a source-code mirror.
7. A repo is only marked current after its intended upstream was fetched and a safe fast-forward completed or its divergence was explicitly recorded.

## Current transfer blockers

- Gateway sudo is not currently saved; root-owned project content and Git metadata cannot be completely audited or updated until one-time sudo is approved.
- No GitHub HTTPS credential is stored in Gateway; VPS HTTPS fetch/push to private forks cannot authenticate.
- VPS SSH GitHub host-key trust is not configured; SSH Git push was not attempted.
- GitHub connector is installed and has push permission for the private target, but it does not expose a bulk local-folder upload or Git push endpoint. It can write individual blobs/trees/commits.
- The target branch is an inventory checkpoint. No complete source repository has yet been mirrored into it.

## Relevant app/tool status

- GitHub connector: installed and enabled.
- Firecrawl: installed and enabled.
- Vercel: installed and enabled.
- Parallel Search: connected search tool available.
- Gateway SSH: connected to `agent-vps`.
- PR Completion: installed skill available for review/commit workflows.
- Additional app installations or permission escalation are not required to use these connected tools. Never enable blanket full-access permissions merely to complete a repository transfer.
