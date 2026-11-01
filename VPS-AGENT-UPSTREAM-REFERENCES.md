# Verified public Agent upstream references

Repository: `0megAlpha/-`
Branch: `vps-mirror/inventory-2026-11`
This file records exact public upstreams discovered while reconnecting to the VPS. It is a reference index, not a full local-source mirror.

| Intended folder | Public repository | Default branch | Verified HEAD | Local VPS relationship |
|---|---|---|---|---|
| `hermes/` | https://github.com/NousResearch/hermes-agent | main | `c627ec84664d43e0b18b95d9d86d8963747d56c7` | Local `/home/xiaye/hermes-007` is on master at `e6f0042db752885c072a782fd7ede1b17350e7c3`, 22 behind upstream; two untracked secrets-guide directories are preserved locally |
| `openhands/core/` | https://github.com/OpenHands/OpenHands | main | `cdd6a69248ce8f99b41ff4c47bdf68dee95024e5` | Current public core; distinct from the VPS v1.25.0 release snapshot and integrated deployment |
| `openhands/software-agent-sdk/` | https://github.com/OpenHands/software-agent-sdk | main | `98849457621881ae2414719b82b8bc1cf535b4ab` | Official SDK repository |
| `openhands/extensions/` | https://github.com/OpenHands/extensions | main | `6fb2b67680b9a5b41452a148e5705f99c7df1a75` | Matches local `/home/xiaye/openhands-extensions` HEAD last verified; Gateway fetch is currently blocked by lock conflict |
| `CKA-Agent/` | https://github.com/Graph-COM/CKA-Agent | main | `938becd7011e834ed9cf89140e9fdddc12a2866c` | Matches VPS HEAD; local modified config and backup remain uncommitted and are not part of this reference |

## Why these are references, not a completed mirror

Public repo metadata and HEAD commits can be verified via GitHub, but this does not migrate VPS-only changes, untracked files, local branches, submodules or Git history into the private target. Private VPS origins under `xh09411-web` are not accessible to the configured Gateway credential.

## Still not mirrored

- `Ai-agent-skill/`: one local commit ahead, 24 behind, modified `push.sh`, and seven untracked source paths.
- `Google-AI/`: 2,563 staged paths including a submodule/gitlink. No commit, reset or pull has been run.
- `Claude-code/`: clean local checkout; configured private origin returned repository-not-found to current Gateway credentials.
- `All-in/`, `agent-plane/`, `sentinelx-cloud-core/`: root-owned and not fully inspected in this session.
- Hermes custom untracked secret-guide paths are excluded pending review.
- The OpenHands integrated and v1.25.0 deployment snapshots remain separate and require source/history review.

## Safe checkout

Once the submodule pointers are deliberately committed in this target repository, initialize with:

```bash
git clone --recurse-submodules --branch vps-mirror/inventory-2026-11 https://github.com/0megAlpha/-.git
```

That command is not yet valid for this reference-only commit because no `.gitmodules` file or gitlink entries have been added here.
