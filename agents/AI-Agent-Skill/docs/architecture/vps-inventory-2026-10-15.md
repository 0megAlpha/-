# VPS Agent Inventory — 2026-10-15

This is an observed inventory snapshot, not a statement that integration is complete.

## Reachability

- SentinelX: one operational host, greencloud-ai.
- Termalin: one online greencloud-ai tunnel and one offline tunnel with the same name. The offline endpoint could not be inspected.
- Desktop Commander: one online device and two offline devices, all named greencloud-ai.
- Therefore, this run can verify the online VPS only; other/offline VPSs remain unverified.

## Storage and recovery

- Root filesystem: 310 GB total; about 40 GB available at inventory time.
- Pre-change backup: /root/migration-safety/20261015-002043/canonical-agent-integration/.
- It contains Git bundles and working-tree archives for open-hands, hermes-007, AI-Agent-Skill and the integrated OpenHands checkout, plus OpenHands state/skills and relevant service/proxy configuration. Verify SHA256SUMS before recovery.
- Do not delete old state directories or Docker volumes until ownership, contents, and restore procedures are verified.

## Observed OpenHands-related containers

- openhands: custom image ai-agent-snapshots/openhands-pre-api:20261009-053318, loopback port 3000.
- openhands-canvas-browsermcp-canary-20261014: patched Agent Canvas 1.27.1 image, loopback port 8009.
- openhands-canvas-mcp-canary-20261013: Agent Canvas 1.25.0, loopback port 8004.
- openhands-canvas-canary-20261012: Agent Canvas 1.25.0, loopback port 8003.
- openhands-canvas-staging: staging image, loopback port 8001.
- stoic_colden and affectionate_chatelet: unlabelled-name Agent Canvas 1.25.0 containers without published host ports.
- These instances use different state/project mounts. Do not remove any until state migration and final UI/API verification pass.

## Observed services and security concerns

- hermes-api.service, hermes-gateway.service, dsh-agent.service, local model services, LiteLLM bridge, SentinelX and Termalin were active.
- openhands-watchdog.service was activating at inventory time; its timer is installed.
- Ports 8444 and 8445 bind to the Tailscale IP. 3000, 8001, 8003, 8004 and 8009 bind to loopback.
- new-api (3001) and openhands-invariant-server (33601) were published on 0.0.0.0; these require a separate access-policy review before changes. Do not close them blindly because clients may depend on them.
- No public push, repository visibility change or destructive cleanup was performed during inventory.

## Repository state observed

- Canonical private repositories are confirmed private through GitHub metadata: open-hands, hermes-007, Ai-Agent-Skill.
- /root/open-hands has untracked reusable skills; preserve and classify them before moving.
- /opt/open-hands-integrated-main contains local changes to oh-my-agent skill listing plus tests; preserve those changes and merge them into the appropriate capability repository after verification.
- Several AI-Agent-SKILL working copies/branches diverge. Do not force-push; merge by content and secret-scan first.
