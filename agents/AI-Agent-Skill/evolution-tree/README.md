# Agent Evolution Tree

Purpose: continuously improve custom agents without merging identity, memory, credentials, or runtime boundaries.

## Loop
DISCOVER -> BASELINE -> PROPOSE -> SANDBOX -> EVAL -> VERIFY -> REFLECT -> VERSION -> MEMORY_UPDATE -> PROMOTE/ROLLBACK

Every generation must have a parent, immutable evidence, fitness score, changed skills/config, and verification result. No self-modification is promoted directly into production. Production promotion requires a passing evaluation and rollback point.

## Boundaries
- Identity, memory, credentials and workspace remain agent-scoped.
- AI-Agent-Skill is shared capability only.
- Skills can be inherited; secrets cannot.
- Failed generations remain recorded, never silently overwritten.
