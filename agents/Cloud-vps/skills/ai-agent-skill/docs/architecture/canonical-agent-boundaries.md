# Canonical Agent Architecture and Repository Boundaries

Status: integration baseline drafted 2026-10-15; local-only, not pushed.

## Canonical ownership

1. xh09411-web/open-hands (private): OpenHands deployment configuration, sandbox/workspace configuration, AGENTS.md, Compose/systemd, reverse-proxy templates, CI/CD and small, reviewable patches against official OpenHands. Do not use it as a full upstream source-code mirror. Keep upstream code as a pinned dependency/image or temporary build checkout; keep custom reusable plugins/skills in AI-AGENT-SKILL.
2. xh09411-web/hermes-007 (private): user's Hermes deployment/configuration, gateway, plugin configuration, memory policy, scripts and workflows. Upstream references: NousResearch/hermes-agent and vectorize-io/hindsight. Do not mirror/fork upstream wholesale.
3. xh09411-web/Ai-Agent-Skill (private; canonical repository for all other agents' reusable capabilities): skills, prompts, SOPs, policy, workflows, plugin/tool/function manifests, adapters and integration tests. OpenHands/extensions is an upstream reference/source for official skills, not a repo to fork wholesale.
4. User-built agents: current VPS evidence identifies DSH (dsh-agent.service, repo --dsh) and CUGA (-cuga-agent- repo) as the likely two custom runtimes. Preserve them as their own runtimes; their reusable skills, tools, plugins and SOPs belong in AI-AGENT-SKILL. If the user later identifies different custom agents, update this mapping before moving data.
5. Exactly one final OpenHands runtime/UI is to remain after cutover. Temporary validation containers may be used only during migration and must be removed after a verified cutover. Hermes and the two user-built agents are separate by design; this does not authorize multiple OpenHands versions.

## AI-AGENT-SKILL directory contract

- agents/<agent-id>/: agent-specific manifests, adapters, install/upgrade/verification scripts and compatibility notes.
- skills/<skill-id>/SKILL.md: reusable skills with metadata and provenance.
- prompts/<agent-id>/: system/developer/task prompts; no credentials.
- sop/<domain>/: repeatable operating procedures.
- policies/: security, privacy, redaction, approval and network policies.
- workflows/<workflow-id>/: orchestration definitions and test fixtures.
- plugins/<ecosystem>/<plugin-id>/: plugin metadata, pinned source reference, license, checksums and install/rollback instructions.
- tools/<tool-id>/: tool/function adapters and schemas, with explicit read/write/network scope.
- integrations/<provider>/<integration-id>/: connectors, auth method references and health tests; never commit tokens.
- deploy/: non-secret deployment manifests, version pins and port policy.
- inventory/: generated inventories of repositories, hosts, packages, skills, plugins, tools and their ownership.
- upstreams/ or upstreams-research/: read-only upstream snapshots/research only when licensing and size justify it; never mistake these for user-owned deployable code.

## Required handling rules

- All three canonical GitHub repositories must stay private. Never publish, flip visibility, force-push, or push to an unverified remote.
- No secrets in Git: environment files, tokens, private keys, cookies, local memory databases and runtime state are excluded. Use environment references/secret stores and redact scan output.
- Preserve current working trees and uncommitted customizations before merging. Do not overwrite a dirty tree or use destructive synchronization.
- Before updating a component: record current version, upstream version, license, checksum, dependencies and rollback path; run its tests and integration checks.
- Every integration must declare owning agent, runtime/deployment location, required permissions, network exposure, secret references, health check and rollback procedure.
- ChatGPT apps/connectors (e.g. GitHub, Termalin, Gateway, Replit) are not automatically installable VPS packages. Catalogue them as external connectors and verify their own account authorization separately.
- Do not claim a plugin/tool is integrated merely because its repository or package is present. Integration requires a successful health/tool invocation test.
