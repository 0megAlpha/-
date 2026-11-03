#!/usr/bin/env python3
"""Ghost Gateway — 去敏感 header + debug stream 打包。"""
from typing import Dict, Any
__all__ = ["GhostGateway"]
SENSITIVE_META = frozenset({
    "authorization","x-api-key","x-real-ip","x-forwarded-for",
    "user-agent","referer","origin","cookie","set-cookie"})

class GhostGateway:
    def __init__(self, strip_meta: bool = True):
        self.strip_meta = strip_meta
    def sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        if not self.strip_meta: return dict(headers)
        return {k: v for k, v in headers.items() if k.lower() not in SENSITIVE_META}
    def package_debug_stream(self, body: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        return {"stream": "debug",
                "meta": {k: v for k, v in meta.items() if k.lower() not in SENSITIVE_META},
                "body": body}
    def unwrap_debug_stream(self, packet: Dict[str, Any]) -> str:
        return packet.get("body", "")
