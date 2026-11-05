# VPS Agent Mirror

Private aggregation repository for the VPS Agent ecosystem.

## Full upstream source repositories (Git submodules)

These folders are pinned to verified upstream commits. Clone with `--recurse-submodules` to download their complete source trees and Git history.

| Folder | Upstream | Pinned HEAD |
|---|---|---|
| `hermes/` | https://github.com/NousResearch/hermes-agent | `c7c7e0fa92f40c8f526e4a52c0966c128245ffd3` |
| `openhands/core/` | https://github.com/OpenHands/OpenHands | `cdd6a69248ce8f99b41ff4c47bdf68dee95024e5` |
| `openhands/software-agent-sdk/` | https://github.com/OpenHands/software-agent-sdk | `98849457621881ae2414719b82b8bc1cf535b4ab` |
| `openhands/extensions/` | https://github.com/OpenHands/extensions | `6fb2b67680b9a5b41452a148e5705f99c7df1a75` |
| `CKA-Agent/` | https://github.com/Graph-COM/CKA-Agent | `938becd7011e834ed9cf89140e9fdddc12a2866c` |

## VPS-local mirrors still pending

- `Ai-agent-skill`: one commit ahead / 24 behind; modified `push.sh`; seven untracked paths. Its configured private origin is not accessible with the currently stored Gateway credential.
- `Claude-code`: clean local checkout, but configured private origin is not accessible with the currently stored Gateway credential.
- `Google-AI`: 2,563 staged paths including submodule/gitlink state; not migrated yet.
- `hermes-007`: local branch is 22 commits behind upstream; two untracked secrets-guide directories must be reviewed before inclusion. Upstream fetch has now completed.
- `openhands-extensions`: local working tree clean; fetch from origin completed and updated 31 remote-tracking refs.
- `CKA-Agent`: upstream fetch completed with no ref changes; local config modification and backup remain uncommitted.
- `All-in`, `agent-plane`, `sentinelx-cloud-core`: root-owned; require complete source inventory and safe snapshot.
- OpenHands integrated and v1.25.0 deployment snapshots remain separate from upstream core.

## Browser clone

```bash
git clone --recurse-submodules --branch vps-mirror/inventory-2026-11 https://github.com/0megAlpha/-.git
```

## Safety

No credentials, .env files, private keys, tokens, databases, runtime sessions or logs are included. Submodules preserve the upstream repositories and pinned commits, but do not include VPS-local modifications. This is a partial upstream-source mirror, not yet a complete VPS-local mirror.


## Deployment records

- [Uploaded Agent deployment guide](docs/source/Agent部署.md) — source-preserved upload; installation steps and third-party plugin compatibility remain to be verified on this VPS.
- [Deployment status and handoff](docs/DEPLOYMENT-STATUS-2026-11-05.md) — verified GitHub write, VPS sync blockers, security notes, and remaining work.
