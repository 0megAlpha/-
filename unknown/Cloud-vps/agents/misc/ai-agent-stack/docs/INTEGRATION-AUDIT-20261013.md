# Agent / Tool Integration Audit — 2026-10-13

## Scope and evidence standard

This audit combines live checks on VPS host greencloud-ai, the current GitHub repository state, Lody CLI inspection, ChatGPT connector/plugin discovery, and the existing execution tracker. "Installed", "configured", "running", "API-tested", "tool-tested", and "end-to-end verified" are distinct states. Empty CI results are not treated as successful CI.

## Engineering audit matrix

| Module / service | Current evidence | Status | Git / deployment state | Remaining risk |
|---|---|---|---|---|
| GitHub target repository | xh09411-web/ai-agent-stack; private repository; push permission confirmed | Connected | Branch portable-20260924 pushed and clean; latest commit recorded below | Latest commit has no reported status checks or PR workflow runs |
| PR #4 | Closed and merged; merge commit e2d9d3c1270487ceb43556bac2625f3bd15dfc84 | Merged | GitHub confirms merged | No CI checks reported by connector |
| Codex local wrapper | Local LiteLLM Responses API call and file create/read test passed in prior live validation | Direct path tested | Wrapper and progress timer included in merged PR #4 | Default root Codex profile remains unauthenticated on unavailable sim provider; mobile Remote Control not verified |
| Local Qwen3-4B inference | llama-agent-fast.service active; authenticated /v1/models returns qwen3-4b-local | Running / API verified | Context override deployed at 32768 and included in repo | Larger context increases memory use; model is CPU-bound and tool-rich prompts can be slow |
| Claude Code CLI | Direct one-shot and restricted shell-tool create/read tests succeeded with CLAUDE_CODE_SIMPLE=1 | Direct CLI tested | Deployment notes committed | Custom alias my-model still emits a non-fatal unrecognized_model warning |
| Lody Claude Code agent config | Non-secret env set to ANTHROPIC_BASE_URL=http://127.0.0.1:4000, ANTHROPIC_MODEL=my-model, CLAUDE_CODE_SIMPLE=1; ACP capability refresh succeeded | Configured, not end-to-end verified | Config is cloud-backed in Lody; local project ai-agent-stack registered | Two read-only ACP sessions timed out at 65s and 75s and were cancelled; investigate latency/context/tool overhead |
| LiteLLM main proxy | systemd active; local Claude Code requests returned HTTP 200 | Running / API tested | Existing config contains local Qwen, NVIDIA, DeepSeek, and slow local-model routes | Virtual-key/database management still reports database not connected; do not copy gateway master key into Lody |
| OpenHands bridge | Readiness previously returned healthy | Partially healthy | Service active | Health payload says db: Not connected; database-backed features are not verified |
| Hermes / DSH / Lody daemons | systemd services active | Running only | Existing services retained | Active status alone does not prove full task completion; prior DSH runtime errors remain to be re-tested |
| n8n | CLI version 2.42.7 | Installed, not running | n8n.service inactive; no listener confirmed on 5678/5679 | Not available as a running workflow service |
| Crush / Kilo CLI | Live commands report Crush 0.98.1 and Kilo/KiloCode 7.8.8 | Executable versions verified | Repair notes committed earlier | /usr/local package metadata still differs from executable payload versions; controlled reinstall remains desirable |
| Promptfoo / TweakCC | Commands report 0.124.1 and 4.4.0 | Version checks passed | Installed globally | Full project-level test runs not demonstrated here |
| Termalin | VPS tunnel to greencloud-ai online; remote shell commands succeed as root | Connected | Live host access | Duplicate greencloud-ai entry is offline; avoid assuming it is the same machine |
| Remote Desktop Commander | One greencloud-ai device online; two entries offline; online device was previously ping-verified | Connected | Device app version 0.2.52 | Mobile-to-Git workflow has not been tested end-to-end |
| Gateway | Historical project notes say VPS-MVP access was revoked | Not used for current VPS work | Termalin used instead | Do not rely on old Gateway credentials or assume old authorized_keys entries were removed |
| GitHub connector | Installed and authenticated; repository read and push access available | Connected | Latest commit pushed | CI status and workflow results are empty, not green |
| Vercel | Connector installed; current project listing returned zero projects | Connected but no project found | No Vercel deployment established | Need a project/repository association before claiming deployment |
| Val Town | Connector responds; current account has zero vals | Connected but no project found | No Val Town deployment established | Create/select a val before integrating |
| Modal | No Modal connector/tool namespace was exposed in current tool inventory | Not integrated here | No deployment evidence | Requires an available connection or explicit project credentials |
| Develoop | Plugin search did not return an exact Develoop match | Not verified | No deployment evidence | Exact product/connector identity remains unresolved |
| Smart Model Router | No exact plugin match surfaced; LiteLLM is the existing model-routing layer | LiteLLM available; named plugin not verified | Routes exist in VPS LiteLLM config | Do not equate LiteLLM routing with the separately named plugin |
| Vibe Coder | No exact plugin match surfaced in plugin search | Not verified | No repo/deployment evidence | Exact connector identity remains unresolved |
| Code Review | No exact ChatGPT plugin match surfaced; GitHub review APIs and Claude Code's code-review command are available | Partial capability available | PR review tools exist | No independent review of the latest commit recorded |
| Session Exporter | Installed skill instructions are available | Skill available | This document is an engineering audit, not a complete raw transcript export | The conversation contains inaccessible/skipped history blocks; do not claim a full chronological transcript export |
| OpenAI Developers / Code | OpenAI Developers connector is installed | Available | No specific project action run in this audit | A generic "Code" label is ambiguous; do not mark a separate product integration complete |

## Environment / runtime inventory

| Component | Observed version or setting | Verification |
|---|---|---|
| Codex CLI | 0.162.1 in existing tracker; default root profile reports Not logged in | Default profile auth failed; isolated local wrapper succeeded |
| Claude Code | 2.1.296 global CLI; Lody ACP bundle reports 2.1.284 | Direct CLI tested; Lody ACP turn did not complete in timeout |
| OpenCode | 1.19.0 in existing tracker | Version recorded, no new runtime test here |
| Crush | 0.98.1 active executable | Version command |
| Kilo / KiloCode | 7.8.8 active executable | Version command |
| n8n | 2.42.7 | CLI version; service inactive |
| Promptfoo | 0.124.1 | CLI version |
| TweakCC | 4.4.0 | CLI version |
| Qwen3-4B llama-server | 127.0.0.1:8089; context 32768 | systemd active; authenticated model list verified |
| LiteLLM main proxy | 127.0.0.1:4000 | systemd active; Anthropic-compatible requests returned HTTP 200 |
| Lody Claude Code environment | ANTHROPIC_BASE_URL, ANTHROPIC_MODEL, CLAUDE_CODE_SIMPLE | Lody config output confirms values; no auth token stored in Lody cloud config |
| Root disk | 310 GB filesystem, 267 GB used, 43 GB free (87%) | df -h / |

## GitHub push evidence

- Repository: https://github.com/xh09411-web/ai-agent-stack
- Branch: portable-20260924
- Latest commit: 5030d7aeb34c199a6a91d614a138b02ba48ec5de
- Commit message: fix: tune local Claude Code context and document Lody setup
- Working tree was clean and branch synchronized with origin after push.
- GitHub combined status returned an empty statuses list and workflow lookup returned no workflow runs for this commit. CI is therefore unreported, not passed.

## Immediate action list

- [ ] Diagnose why Lody ACP requests do not finish within 65–75 seconds despite successful local Claude Code tests and successful LiteLLM HTTP requests.
- [ ] Run a Lody session that executes one safe terminal read and returns the result before calling Lody end-to-end functional.
- [ ] Resolve or document the custom model alias warning and confirm how ACP selects model/context settings.
- [ ] Repair the LiteLLM database/virtual-key path only with a backup and a controlled rollback plan.
- [ ] Fix the OpenHands bridge database connection and test an actual database-backed operation.
- [ ] Authenticate the default Codex profile or formally standardize on the tested isolated codex-local wrapper; do not overwrite the existing default config blindly.
- [ ] Test the phone-to-Lody/Codex-to-VPS-to-Git push path from the user-facing client.
- [ ] Investigate the nine outdated global npm packages individually; do not perform blanket major upgrades.
- [ ] Schedule the required host reboot only after checking service recovery and maintenance impact.
- [ ] Re-check disk usage and only remove caches/artifacts after dependency and rollback review.

## Acceptance rule

No agent is considered fully integrated until it can receive a task through its intended entry point, execute the required tools against the intended project, produce a verifiable artifact or repository change, pass the relevant tests, and report a recoverable failure path. Service-active status and catalog availability are not acceptance evidence.
