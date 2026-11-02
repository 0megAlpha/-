# AGENT//THRONE File & Conversion Center

Portable service boundary for the iPhone-first AI OS.

## Responsibilities
- Upload/download and resumable transfer boundary.
- File metadata and safe preview endpoint.
- Background conversion jobs with progress polling.
- Optional adapters for FFmpeg, ImageMagick, LibreOffice, 7-Zip/bsdtar, and Android tooling when present.
- Explicit IPA inspection/rebuild workflow. **IPA is not a binary format that can generally be converted directly to APK.** A true iOS→Android port requires source code and an Android build target; the service therefore never pretends to perform a binary conversion.
- WebSocket/SSE-ready job event model through `/api/jobs/{id}` polling and `event_seq` fields; frontend can later upgrade to WebSocket without changing the job contract.

## Security boundary
The service is designed to run behind the AGENT//THRONE auth/policy gateway. It does not expose host shell execution. Conversion commands are selected only from a fixed adapter registry. Uploaded files are treated as untrusted.

## API
- `GET /health`
- `POST /api/files` multipart upload (`file`)
- `GET /api/files/{id}` metadata
- `GET /api/files/{id}/download`
- `GET /api/files/{id}/preview`
- `POST /api/jobs` JSON `{file_id, operation, options}`
- `GET /api/jobs/{id}` progress/state
- `POST /api/jobs/{id}/cancel`
- `GET /api/capabilities`

Operations are intentionally capability-driven rather than arbitrary shell commands.

## Run
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r app/requirements.txt
uvicorn app.server:app --host 127.0.0.1 --port 8890
```

The service should be bound to loopback/private network and published through the existing AGENT//THRONE gateway, never directly to the public internet.
