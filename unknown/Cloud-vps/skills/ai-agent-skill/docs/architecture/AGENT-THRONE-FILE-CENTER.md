# AGENT//THRONE File Center

Portable conversion/file inspection service integrated as an internal capability.

- systemd service: `agent-throne-file-center.service`
- bind: `127.0.0.1:8890` only
- storage: `/opt/agent-throne-file-center/storage`
- runtime user: `agentthrone-file`
- default external port exposure: none
- source: `integrations/file-center/`
- deployment releases are versioned under `/opt/agent-throne-file-center/releases/`
