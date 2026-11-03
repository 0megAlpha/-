# Linux VPS Rebuild Inventory

Captured 2026-10-11. This is a sanitized snapshot of currently running containers and their rebuild dependencies. It deliberately excludes secret values, user/session contents, host addresses, and credential material.

## Purpose

The target is a portable Linux deployment in which Agent frameworks, shared Skills, MCP/tool integrations, and collaboration services can be restored from GitHub and pinned dependencies. Operators should only need to provide environment-specific values such as API keys, tokens, domain names, and storage paths through untracked secret files or a secret manager.

## Runtime snapshot

See `../portable/vps-export/manifests/runtime-containers.tsv` for container image references, immutable image digests, source metadata, and known configuration paths.

See `../portable/vps-export/manifests/runtime-state-map.tsv` for persistent state that must be mapped before any cleanup or rebuild.

## Local inference baseline (verified 2026-10-13)

- The original 27B Q8 GGUF model remains at `/opt/qwen38-runtime/Qwen3.8-27B-EfficientThink-SimPO-Q8_0.gguf` on port `127.0.0.1:8088`; on this 4-vCPU CPU-only VPS it is too slow for interactive Agent tool use and is retained as a fallback, not removed.
- A separate Qwen3-4B Q4_K_M service is installed from the official `Qwen/Qwen3-4B-GGUF` Apache-2.0 artifact at `/opt/qwen3-4b-runtime/`, loopback port `127.0.0.1:8089`. Its API key file is outside Git at `/etc/llama-agent-fast/api-keys`, mode `0600`.
- LiteLLM alias `my-model` now routes to `qwen3-4b-local`; `my-model-slow` preserves the 27B endpoint. Qwen thinking is disabled through `chat_template_kwargs.enable_thinking=false` so short calls return final content instead of reasoning-only output.
- Verified: direct fast-model request returns HTTP 200; unauthenticated direct model catalog returns 401; live LiteLLM and OpenHands bridge tests passed text generation, required function-tool emission, and continuation after a simulated tool result. This is not yet a real OpenHands UI task, shell-tool execution, or mobile-to-Git end-to-end acceptance test.
- The NVIDIA and DeepSeek provider variables still contain non-ASCII placeholder-like values, and Codex CLI remains unauthenticated with its `sim` endpoint at `127.0.0.1:4010` unavailable. External-provider and Codex tasks remain blocked until credentials/provider setup are corrected.
- Hermes CLI now has a recognized custom provider entry (`local-litellm` → `127.0.0.1:4000/v1`, model `my-model`, key source `OPENAI_API_KEY`) and LiteLLM drops unsupported request parameters for this local model. A narrow one-shot test passed only with `--ignore-rules -t terminal`. Full Hermes prompts exceeded the current 8,192-token server context (observed 18,511 and 32,943 tokens), so the default full-toolset Hermes flow is still not accepted as working. The `hermes-gateway.service` unit does not currently load `/root/.agent.env`; no production gateway restart was done because that file contains multiple provider/channel secrets.
- Lody's agent-config catalog lists ten agent configs as available, but availability metadata is not a successful inference/task test. No credentials were pushed to the Lody cloud config store.
- Do not commit model weights, `.agent.env`, or the generated API key. The reproducible service and LiteLLM fragment are under `deploy/local-qwen-fast/`.

## Current rebuild blockers

1. **OpenHands custom image** — `ai-agent-snapshots/openhands-pre-api:20261009-053318` is locally named and has no OCI source/revision labels. Its Dockerfile/build context and patch set have not yet been located. Do not delete its image or source candidates until provenance is recovered or the image is reproducibly rebuilt.
2. **Agent Canvas staging image** — `openhands-canvas:staging` has an OpenHands source/revision label, but the exact local build recipe and changes that produced this image are not yet established.
3. **Agent Plane/Caddy** — the active Caddyfile is mounted from a local repository with no Git remote and has local changes. The same directory contains a separate secret file; only a sanitized configuration template may enter Git.
4. **All-in/Qdrant** — the active Compose file is under the All-in checkout, whose secondary working copy has local changes. Reconcile the active configuration into a feature branch and record the Qdrant state-volume restore procedure.
5. **Open Terminal and Conduit** — persistent state is mounted, but the complete declarative launch configuration has not yet been identified.
6. **Image mutability** — several deployed images use mutable tags such as `latest` or `main`. Digests are recorded for this snapshot; future deployment files should pin digests or an explicitly reviewed version.
7. **Non-container Agent runtimes** — Hermes, CLI tools, MCP servers, scheduled jobs, and user-level configuration still need a complete package/version/entrypoint inventory before this manifest can be considered complete.

## State and source-control rules

- Source, Skills, plugins, workflow definitions, safe configuration templates, version pins, bootstrap scripts, health checks, and restore instructions belong in Git when licensing and secret scanning permit.
- API keys, tokens, private keys, `.env` files with real values, session logs, conversation state, user data, vector database contents, runtime databases, model weights, Docker volumes, and backup archives do not belong in Git.
- Use `.env.example` with clearly nonfunctional placeholders. Keep actual secrets in a local file with restrictive permissions or a dedicated secret manager.
- Do not delete a local source tree merely because a remote branch exists. First verify the exact commit/file content on GitHub, determine whether local-only changes are needed, and confirm that no active process, container build, scheduled task, or restore procedure references the path.
- Exact duplicate bytes prove file identity, not that either copy is unused. For backups, retain at least one integrity-checked canonical copy until the associated recovery purpose is retired.

## Migration workflow

1. Inventory the live service and its actual configuration/state sources.
2. Compare each intended repository against the current GitHub branch SHA, not only stale local tracking refs.
3. Classify local-only files into source, upstream dependency, cache/download, runtime state, backup, or secret.
4. Scan the proposed tree, index, and Git history. Review candidate findings without displaying secret values.
5. Add only sanitized, required content on a new feature branch; run validation and inspect the exact diff.
6. Push the branch, verify the remote SHA and files, and open a pull request. Do not merge automatically.
7. Verify a clean Linux rebuild and core Agent capabilities before deleting redundant local source/download files.
8. Record disk usage before and after each explicitly scoped cleanup. Never prune active Docker volumes or images solely because Docker labels them reclaimable.
