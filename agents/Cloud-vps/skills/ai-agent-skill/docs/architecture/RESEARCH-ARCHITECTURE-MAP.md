# Research Architecture Map

These upstreams are reference/candidate integrations, not source-tree merges.

| Upstream | Integration role | Default |
|---|---|---|
| BitDecoding | long-context/low-bit decoding research reference | candidate |
| Tinder StateMachine | deterministic FSM/state/effect patterns | enabled in architecture |
| HyperAgents | multi-agent orchestration/evolution research | candidate |
| hyperagent-public-skills | reusable agent skills | opt-in |
| Live-SWE-agent | runtime self-evolution loop reference | candidate |
| PySR | symbolic regression/search | opt-in |
| ModelingToolkit.jl | symbolic modeling/transform reference | opt-in |
| PentestGPT | authorized security-agent pipeline reference | sandbox/manual |
| FuzzingBrain | fuzzing + suspicious-point + verification reference | sandbox/manual |

The repositories remain independent. Only adapters, contracts, skills and documented patterns are integrated into Ai-Agent-Skill.
