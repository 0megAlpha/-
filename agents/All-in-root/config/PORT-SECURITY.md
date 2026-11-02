# VPS port and exposure policy

| Port | Service | Intended exposure |
|---:|---|---|
| 22 / 2222 | SSH | Public SSH remains enabled for current administration; use key authentication, disable password login where confirmed safe, and keep an out-of-band recovery path |
| 3000 | OpenHands | Tailscale/private overlay only; public-interface Docker traffic blocked by `agent-docker-port-guard.service` |
| 3001 | New API | Tailscale/private overlay only; public-interface Docker traffic blocked |
| 33601 | OpenHands invariant server | Tailscale/private overlay only; public-interface Docker traffic blocked |
| 4000 | LiteLLM | Loopback only (`127.0.0.1`) |
| 4001 | OpenHands → LiteLLM bridge | Private Docker bridge address only |
| 6333 / 6334 | Qdrant | Loopback only (`127.0.0.1`) |
| 8000 | Open terminal service | Loopback only (`127.0.0.1`) |
| 8081 | OpenWebUI | Tailscale interface only |
| 80 / 443 | Reverse proxy / Tailscale | Do not add public ingress without explicit review |

The guard service inserts idempotent `DOCKER-USER` rules for new TCP connections arriving through the public interface to original destination ports 3000, 3001, and 33601. It does not block Tailscale-interface traffic or change SSH. A backup of the prior iptables rules is stored under `/root/ai-system-audit/backups/`.

Docker port bindings may still show `0.0.0.0`; the guard is a packet filter, not a bind-address change. Verify the guard service after Docker restarts and from an external network before considering exposure testing complete. Qdrant's Compose definition in this repository now binds only to loopback for future recreations.
