# Browser MCP compatibility patch for OpenHands Agent Canvas

Owner: private AI-AGENT-SKILL repository.
Base image: ghcr.io/openhands/agent-canvas:1.27.1
Base image digest observed 2026-10-15: sha256:91b7a217dcbefe8c10562523b043458ed1dfaf8ba770194b319fe754cee03f23
NPM dependency: @browsermcp/mcp@0.1.3 (registry latest verified on 2026-10-15).

The upstream package has two runtime issues in this deployment:
1. It kills processes by port without handling an empty PID list.
2. Its server close override recursively calls itself.

The patch guards the empty PID list and calls a bound original server close method. The patch intentionally changes no MCP tools or access scope. The image build installs lsof, pins the package version, applies the patch, and runs Node syntax validation.

Build from this directory:
  docker build -t ai-agent-snapshots/agent-canvas:1.27.1-browsermcp-fixed-20261015 .

Verify:
  node --check /opt/browsermcp/node_modules/@browsermcp/mcp/dist/index.js
  OpenHands SDK MCP discovery should return 12 Browser MCP tools.
  Direct MCP initialize + tools/list + clean shutdown must pass.
