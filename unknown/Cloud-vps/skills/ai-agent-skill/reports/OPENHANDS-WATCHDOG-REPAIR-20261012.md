# OpenHands watchdog safety repair — 2026-10-12

## Root cause
- The existing /usr/local/bin/openhands-watchdog.sh accepted no arguments, so --dry-run was not a dry-run; it still invoked container starts, a Tailscale daemon restart, and Tailscale Serve reconfiguration when checks appeared unhealthy.
- The script had no single-run lock. The 5-minute systemd timer was enabled; the last recorded service run exited successfully.
- The watchdog log showed repeated Tailscale Serve reconfiguration notifications. Current read-only status showed the expected 127.0.0.1:8443 target present.

## Backup
- Script backup: /root/ai-company/backups/openhands-watchdog-before-dry-run-20261012.sh
- Service unit backup: /root/ai-company/backups/openhands-watchdog-service-before-dry-run-20261012.service

## Change
- Added --dry-run and --help; unknown arguments now exit with status 2.
- Dry-run still performs read-only state checks but prints planned actions and does not execute recovery commands, write the watchdog log, or send Hermes notifications.
- Added a flock lock for normal (mutating) runs to avoid overlapping timer/manual invocations.
- Added environment overrides for log and lock paths so the test harness can isolate side effects.
- Preserved the existing default recovery behavior; no systemd unit or timer was changed and no service/container restart was issued during this repair.

## Test evidence
- Test-first red: before the implementation, bash /root/ai-company/scripts/test-openhands-watchdog-dry-run.sh failed because the supposedly dry-run invocation recorded docker start, systemctl restart, and tailscale serve --bg calls in the stubbed command log.
- Green: the same test now reports PASS: dry-run reports recovery actions without invoking them or writing logs.
- bash -n /usr/local/bin/openhands-watchdog.sh passed.
- openhands-watchdog.sh --help exited 0.
- Real-system openhands-watchdog.sh --dry-run exited 0 with no planned recovery actions printed.
- Script mode remains 755 root:root.

## Remaining risks
- Normal mode intentionally retains automatic recovery actions. The port exposure audit remains open: Docker currently publishes new-api on host port 3001 and openhands-invariant-server on host port 33601 on all IPv4/IPv6 interfaces. External reachability was not independently tested; do not change these bindings until their required clients are confirmed.
- Host listeners on 8888, 8743 (ENI Harbor), 42363 (Lody Agent), and 631 (CUPS) bind all interfaces; UFW defaults to deny incoming and has no explicit allow for those ports, but external reachability still needs independent validation.
## Source-control boundary
- GitHub code search for `openhands-watchdog.sh` and `ai-agent-upstream-check` returned no matching tracked files in accessible default branches. The live watchdog repair therefore remains on the VPS with a local backup and report; it has not been pushed into an arbitrary repository. A canonical deployment/source repository must be selected before syncing this system script to GitHub.
