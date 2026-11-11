# Architecture

~~~text
User / iOS / Lody-Conduit (pending exact API verification)
                  |
           Dify Workflow UI
                  |
        LangGraph control plane
         |              |
     LiteLLM          policy/review
         |
  OpenAI-compatible model providers
                  |
        OpenHands execution agent
                  |
    isolated workspace / Docker runtime
                  |
    pytest + Ruff + Playwright + Semgrep
                  |
      Gitleaks + Trivy + human review
                  |
      GitHub (0megAlpha repositories)
~~~

## Responsibilities

- OpenHands: repository-aware coding and terminal execution.
- LangGraph: typed state, explicit transitions, bounded correction cycles.
- LiteLLM: model/provider routing; credentials remain server-side.
- Dify: visual workflows, input forms and operator visibility.
- AutoGen/Magentic-One: optional specialist-agent experiments; not the primary coordinator.
- Aider: optional multi-file terminal editing, invoked inside the selected project workspace.
- Playwright: browser and end-to-end verification.
- Semgrep, Gitleaks, Trivy: static analysis, secret detection and image/filesystem vulnerability scanning.

## Non-goals

No claim of MCTS or reinforcement-learning training is made. The review graph is a bounded LLM workflow, not a Monte-Carlo search engine. No automatic production deployment or port publication occurs.
