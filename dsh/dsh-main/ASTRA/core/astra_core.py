#!/usr/bin/env python3
"""ASTRA Core — 把六个模块串成 pipeline。纯 library，不监听端口。"""
import json, os, sys
from typing import Any, Dict, List

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path: sys.path.insert(0, _HERE)

try:
    from .adversarial_engine import AdversarialEngine
    from .ghost_gateway import GhostGateway
    from .realm_decomposer import RealmDecomposer
    from .outbound_cloaker import OutboundCloaker
    from .metacipher_engine import MetaCipher
    from .cka_agent import CKAAgent
except ImportError:
    from adversarial_engine import AdversarialEngine
    from ghost_gateway import GhostGateway
    from realm_decomposer import RealmDecomposer
    from outbound_cloaker import OutboundCloaker
    from metacipher_engine import MetaCipher
    from cka_agent import CKAAgent

__all__ = ["AstraCore"]

class AstraCore:
    def __init__(self, cfg: Dict[str, Any] | None = None):
        cfg = cfg or {}
        self.jbfuzz  = AdversarialEngine(seed=cfg.get("seed", "dsh-jb"))
        self.ghost   = GhostGateway()
        self.realm   = RealmDecomposer(chunk_size=cfg.get("chunk", 3))
        self.cloaker = OutboundCloaker(mode=cfg.get("cloak_mode", "base64"))
        self.meta    = MetaCipher(salt=cfg.get("salt", "dsh-meta"))
        self.cka     = CKAAgent(max_depth=cfg.get("cka_depth", 4))
    def pipeline(self, task: str, keywords: List[str] | None = None) -> List[Dict[str, Any]]:
        keywords = keywords or []
        frags = self.cka.decompose(task)
        woven = self.cka.keyword_weave(" ".join(frags), keywords)
        batches = self.realm.batch(self.realm.decompose(woven))
        cloaked = [self.cloaker.to_tech_log(" ".join(b)) for b in batches]
        packets = [self.ghost.package_debug_stream(c, {"source": "astra"}) for c in cloaked]
        return [self.jbfuzz.wrap_request({"body": p}) for p in packets]
    def health(self) -> Dict[str, Any]:
        return {"version": "5.2.0",
                "modules": ["jbfuzz","ghost","realm","cloaker","meta","cka"],
                "bound": False}

if __name__ == "__main__":
    print(json.dumps(AstraCore().health(), ensure_ascii=False, indent=2))
