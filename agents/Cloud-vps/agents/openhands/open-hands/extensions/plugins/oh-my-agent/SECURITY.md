# Security boundaries

- The MCP transport is stdio only; this package does not open a listening TCP port.
- Provider keys and Mem0 keys are read from environment and never returned by tools.
- Skill listing is read-only. New skills are sanitized drafts only and are not installed or executed.
- Upstream status checks fetch repository metadata only; they do not download or execute upstream code.
- Promotion evidence cannot trigger merge, deploy, or approval. `promotion_allowed` remains false.
- Do not mount `/var/run/docker.sock` into this plugin/evolution worker. Use an isolated sandbox with resource limits and no production network access.
- Pin reviewed dependency versions and images in deployment; avoid `latest` for production.
- Do not expose the MCP server over an unauthenticated network endpoint.
