#!/usr/bin/env python3
"""MetaCipher — 向量/特征哈希混淆。"""
import hashlib, json
from typing import Any, Dict, List
__all__ = ["MetaCipher"]

class MetaCipher:
    def __init__(self, salt: str = "dsh-meta"):
        self.salt = salt
    def _h(self, payload: str) -> str:
        return hashlib.sha256((self.salt + payload).encode()).hexdigest()
    def obfuscate_vector(self, vec: List[float]) -> str:
        return self._h(",".join(f"{v:.6f}" for v in vec))
    def fingerprint(self, features: Dict[str, Any]) -> str:
        return self._h(json.dumps(features, sort_keys=True, ensure_ascii=False))
    def remap(self, code: str, table: Dict[str, str]) -> str:
        return table.get(code, code)
