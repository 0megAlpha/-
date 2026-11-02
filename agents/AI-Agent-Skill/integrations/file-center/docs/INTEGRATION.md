# AGENT//THRONE integration contract

## UI
Add a `File Center` surface behind the existing bottom navigation / project context. It should expose:
1. Upload / download progress.
2. Recent files.
3. Preview.
4. Conversion operation picker based on `/api/capabilities`.
5. Job progress waveform/line graph.
6. Pull/push to the selected workspace/repository through an existing authenticated gateway.
7. Background jobs as a compact dock item, not a permanent dashboard panel.

## Event model
Poll `/api/jobs/{id}` initially. Use `event_seq` to detect updates. Later, proxy the same events over WebSocket/SSE from the AGENT//THRONE gateway.

## Security
- File Center must never be internet-public directly.
- Route through AGENT//THRONE authentication and policy gateway.
- Bind service to loopback/private interface.
- Per-user/project storage namespace.
- Enforce size, type, CPU, memory, timeout and disk quotas outside the conversion worker.
- Never pass arbitrary user strings to shell commands.
- Conversion adapters are a fixed registry.
- Treat uploaded archives and documents as untrusted.
