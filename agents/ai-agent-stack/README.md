# AI Agent Stack — Linux Portability

This repository is the rebuild entry point for the Agent ecosystem: deployment manifests, version pins, sanitized configuration templates, state mapping, validation, and recovery documentation.

## Rebuild contract

A replacement Linux VPS should be rebuildable from versioned source and manifests, then require only separately supplied secrets and environment-specific values. Do not commit API keys, access tokens, private keys, session histories, user data, runtime databases, model weights, Docker volumes, or backup archives.

## Current inventory

- [Linux rebuild inventory](docs/LINUX-REBUILD-INVENTORY.md) records the current running-container baseline and unresolved reproducibility gaps.
- [Safe recovery](docs/SAFE-RECOVERY.md) defines cautious recovery practices.
- [Evolution contract](docs/EVOLUTION-CONTRACT.md) describes repository evolution expectations.

## Important

The runtime inventory is a point-in-time observation, not permission to overwrite production settings. Confirm image digests, configuration sources, persistent-state ownership, and secret placeholders before rebuilding. Runtime state is separate from source control.

## Change policy

Changes are proposed on feature branches and reviewed through pull requests. Never push directly to the default branch or merge a migration PR automatically.
