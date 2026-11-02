"""
title: Parallel Tools
author: Skyzi000
description: 並行執行多個工具調用
version: 1.0.0
"""
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
class Tools:
    def __init__(self):
        self.max_workers = 4
    def execute_parallel(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            fm = {ex.submit(t["function"], *t.get("args", [])): t for t in tasks}
            for fu in as_completed(fm):
                try:
                    results.append({"task": fm[fu], "result": fu.result(), "status": "success"})
                except Exception as e:
                    results.append({"task": fm[fu], "error": str(e), "status": "failed"})
        return results
