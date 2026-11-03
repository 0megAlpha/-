#!/usr/bin/env python3
"""JBFuzz — Base64 封装 + debug log 伪装。纯编解码库，无网络。"""
import base64, re, json
from typing import Dict, Any
__all__ = ["AdversarialEngine"]

class AdversarialEngine:
    def __init__(self, seed: str = "dsh-jb"):
        self.seed = seed
        self.wrap_template = "[DEBUG] trace_id={tid} payload={b64}"
    def encode(self, payload: str, trace_id: str = "0x00") -> str:
        return self.wrap_template.format(tid=trace_id,
            b64=base64.b64encode(payload.encode()).decode())
    def decode(self, wrapped: str) -> str:
        m = re.search(r"payload=([A-Za-z0-9+/=]+)", wrapped)
        if not m: raise ValueError("no payload found")
        return base64.b64decode(m.group(1)).decode()
    def wrap_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        req = dict(req)
        req["_debug"] = self.encode(json.dumps(req, ensure_ascii=False),
                                    trace_id=str(req.get("id", "0x00")))
        return req
