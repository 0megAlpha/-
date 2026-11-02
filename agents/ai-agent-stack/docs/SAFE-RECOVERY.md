# Safe VPS recovery

The default recovery path is the canonical private source, not an image of the expiring VPS.

## Repositories restored by the safe helper

- `Ai-Agent-Skill` (main): canonical skills, adapters, and verification.
- `All-in` (main): SESM/orchestration bundle, dashboards, and safe mobile access guidance.
- `ai-agent-stack` (`portable-20260924`): portable manifests and recovery tooling.
- `ai-agent-fleet` (main): fleet status/workflow CLI. A dirty existing worktree is preserved and skipped.

## Usage

```bash
bash restore/restore-vps-safe.sh
bash restore/restore-vps-safe.sh --apply
```

The first command is a dry run. The second clones missing repositories and fast-forwards only clean worktrees on the expected branch. It never hard-resets, force-pushes, deletes unknown files, creates credentials, opens ports, installs system packages, or starts services.

## After clone

1. Restore API/provider credentials from a password manager or secret manager.
2. Install dependencies into per-project virtual environments.
3. Review service manifests and current port policy before enabling systemd or containers.
4. Run the canonical repository verifier, skill-fleet tests, API compatibility tests, and current VPS smoke checks.
5. Verify real model inference and at least one authorized agent tool-use task before marking the fleet verified.

Do not run the legacy `restore/restore-vps.sh` on a fresh production VPS without reviewing it; it installs packages system-wide and clones several paths directly.
