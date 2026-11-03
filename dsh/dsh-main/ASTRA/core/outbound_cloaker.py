#!/usr/bin/env python3
"""Outbound Cloaker — Hex/Base64 编解码 + 技术日志伪装。"""
import base64, binascii, re
__all__ = ["OutboundCloaker"]

class OutboundCloaker:
    def __init__(self, mode: str = "base64"):
        if mode not in ("base64", "hex"):
            raise ValueError("mode must be 'base64' or 'hex'")
        self.mode = mode
    def encode(self, intent: str) -> str:
        raw = intent.encode()
        return binascii.hexlify(raw).decode() if self.mode == "hex" \
               else base64.b64encode(raw).decode()
    def to_tech_log(self, intent: str, level: str = "INFO") -> str:
        return f"[{level}] cloaked_intent={self.encode(intent)}"
    def decode(self, log_line: str) -> str:
        m = re.search(r"cloaked_intent=([A-Za-z0-9+/=]+)", log_line)
        if not m: raise ValueError("no intent found")
        blob = m.group(1)
        return binascii.unhexlify(blob).decode() if self.mode == "hex" \
               else base64.b64decode(blob).decode()
