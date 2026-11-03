#!/usr/bin/env python3
"""REALM Decomposer — 任务切片 + 批处理。"""
from typing import List
__all__ = ["RealmDecomposer"]

class RealmDecomposer:
    def __init__(self, chunk_size: int = 3):
        if chunk_size < 1: raise ValueError("chunk_size must be >= 1")
        self.chunk_size = chunk_size
    def decompose(self, task: str) -> List[str]:
        lines = [l.strip() for l in task.splitlines() if l.strip()]
        frags = [" ".join(lines[i:i+self.chunk_size])
                 for i in range(0, len(lines), self.chunk_size)]
        return frags or [task]
    def batch(self, fragments: List[str], batch_size: int = 4) -> List[List[str]]:
        return [fragments[i:i+batch_size] for i in range(0, len(fragments), batch_size)]
    def reassemble(self, batches: List[List[str]]) -> str:
        return "\n".join(" ".join(b) for b in batches)
