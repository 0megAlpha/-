"""Ghost Gateway: outbound metadata-stripping proxy (defensive research only)."""
import re
STRIP = re.compile(r'(user-?agent|client|device|session|trace)[-_ ]id', re.I)
def scrub(headers: dict) -> dict:
    return {k: v for k, v in headers.items() if not STRIP.search(k)}
def route(payload: dict) -> dict:
    payload.pop("metadata", None)
    return payload
