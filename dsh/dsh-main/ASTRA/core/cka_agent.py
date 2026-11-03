#!/usr/bin/env python3
"""CKA-Agent clone — 关键词编织 + 自适应树 float搜索。"""
from typing import Any, Callable, Dict, List
__all__ = ["CKAAgent"]

class CKAAgent:
    def __init__(self, max_depth: int = 4):
        if max_depth < 1: raise ValueError("max_depth must be >= 1")
        self.max_depth = max_depth
        self.memory: List[Dict[str, Any]] = []
    def keyword_weave(self, task: str, keywords: List[str]) -> str:
        woven, low = task, task.lower()
        for kw in keywords:
            if kw.lower() not in low:
                woven = f"{woven} [ctx:{kw}]"; low = woven.lower()
        return woven
    def adaptive_tree_search(self, task: str, scorer: Callable[[str],],
                             depth: int = 0) -> str:
        if depth >= self.max_depth: return task
        frags = task.split()
        best, best_score = task, scorer(task)
        for i in range(len(frags)):
            cand = " ".join(frags[:i] + [f"[S{i}]"] + frags[i+1:])
            s = scorer(cand)
            if s > best_score: best, best_score = cand, s
        self.memory.append({"depth": depth, "best": best, "score": best_score})
        return best
    def decompose(self, task: str) -> List[str]:
        return [t.strip() for t in task.split(".") if t.strip()]
