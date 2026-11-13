# OpenHands portable skills — Xiaye integration

This directory contains the vetted, portable Skills installed into the active OpenHands workspace on the VPS.

- Runtime path: `/root/oh-stack/workspace/.openhands/skills/`
- Source: `/opt/agent-integration/staging/agents/AI-Agent-Skill/skills/`
- Installed: **38 Skills**
- Verification: all 38 `SKILL.md` files exist; source files were scanned for secret-patterns before copying. Nine core Skills also passed explicit YAML frontmatter/name/description validation.
- Placeholder-only source directories were excluded from the runtime and are listed in `XIAYE-INTEGRATED-SKILLS.json`.

## Installed Skills

- [agent-fleet-secure-workflow](./agent-fleet-secure-workflow/SKILL.md)
- [agent-readiness-report](./agent-readiness-report/SKILL.md)
- [api-compatibility](./api-compatibility/SKILL.md)
- [cross-repo-testing](./cross-repo-testing/SKILL.md)
- [engineering-memory](./engineering-memory/SKILL.md)
- [firecrawl-web-research](./firecrawl-web-research/SKILL.md)
- [migration-mapping](./migration-mapping/SKILL.md)
- [migration-report](./migration-report/SKILL.md)
- [migration-scoring](./migration-scoring/SKILL.md)
- [agent-skills](./agent-skills/SKILL.md)
- [agentic-security-review](./agentic-security-review/SKILL.md)
- [apollo-memory](./apollo-memory/SKILL.md)
- [build-setup](./build-setup/SKILL.md)
- [cobol-modernization](./cobol-modernization/SKILL.md)
- [composio-tool-integration](./composio-tool-integration/SKILL.md)
- [define-to-ship](./define-to-ship/SKILL.md)
- [ecc](./ecc/SKILL.md)
- [firecrawl](./firecrawl/SKILL.md)
- [harness-evolution](./harness-evolution/SKILL.md)
- [improve-agent-readiness](./improve-agent-readiness/SKILL.md)
- [magic-word](./magic-word/SKILL.md)
- [mainframe-planning](./mainframe-planning/SKILL.md)
- [mainframe-removal](./mainframe-removal/SKILL.md)
- [obra-superpowers](./obra-superpowers/SKILL.md)
- [plan-once-verify-always](./plan-once-verify-always/SKILL.md)
- [score-quality](./score-quality/SKILL.md)
- [score-style](./score-style/SKILL.md)
- [sesm-engine](./sesm-engine/SKILL.md)
- [setup-agents-md](./setup-agents-md/SKILL.md)
- [setup-openhands](./setup-openhands/SKILL.md)
- [setup-pr-review](./setup-pr-review/SKILL.md)
- [skill-optimizer](./skill-optimizer/SKILL.md)
- [to-java-migration](./to-java-migration/SKILL.md)
- [understand-anything](./understand-anything/SKILL.md)
- [upcoming-release](./upcoming-release/SKILL.md)
- [update-sdk](./update-sdk/SKILL.md)
- [vps-bridge](./vps-bridge/SKILL.md)

## Runtime notes

OpenHands already had a set of upstream Skills. This integration adds only missing names and preserves existing Skills. No container restart, new listener, or port change was performed. The workspace mount is persistent, so these files are visible to the existing OpenHands runtime.
