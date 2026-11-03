# Agent Integration Layer

This directory contains adapter and integration metadata. It is not the canonical source tree for the individual Agent runtimes.

## Canonical runtime boundaries

- Hermes: maintained in its own repository and deployed runtime.
- OpenHands: maintained in its own repository and deployed runtime.
- DSH: maintained in its own repository and deployed runtime.
- Claude Code, Codex, OpenCode, Cline, OpenWebUI, Lody, and Conduit: each has its own upstream or runtime boundary.

Do not copy another runtime's source tree into this adapter layer unless a deliberate, license-reviewed vendoring decision is recorded. Use adapters, versioned source references, skills, plugin manifests, workflows, routing metadata, and collaboration protocols to describe integration.

## Vendored plugin marketplace

A snapshot of the MIT-licensed `wshobson/agents` plugin marketplace is kept under [`marketplace/`](marketplace/README.md) as a separately attributed component. Its upstream license is preserved at `marketplace/LICENSE`; review `marketplace/PORTABILITY.md` before syncing or updating it. The upstream `CLAUDE.md` symlink is retained and points to the bundled `AGENTS.md` in this marketplace directory.

## Portability rules

- Use repository-relative paths, pinned source revisions, and environment-variable placeholders.
- Do not commit VPS-specific absolute paths, active credentials, private keys, sessions, logs, runtime databases, or backup archives.
- Keep local adapter metadata distinct from vendored upstream source and record provenance for every vendored component.
