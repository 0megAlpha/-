"""
ResearcherAgent — 網路/文件資料檢索 Agent。

安全：搜尋端點一律從環境變數讀取（SEARCH_API_URL，預設 localhost 佔位），
不內嵌任何真實位址或憑證。mock 模式回傳模擬結果。
"""
import os
import json
from typing import Any, Dict

from agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("researcher", **kwargs)
        self.search_api_url = os.getenv("SEARCH_API_URL", "http://localhost:8000/search")
        self.search_api_key = os.getenv("SEARCH_API_KEY", "YOUR_SEARCH_API_KEY_HERE")

    def _search(self, query: str, limit: int = 5) -> list:
        if self.mock or self.search_api_key.startswith("YOUR_"):
            self.log.info("[mock] 檢索略過: %s", query)
            return [{"title": f"mock-result-{i}", "url": "https://example.com/mock", "snippet": query} for i in range(limit)]
        import requests
        resp = requests.post(
            self.search_api_url,
            headers={"Authorization": f"Bearer {self.search_api_key}"},
            json={"query": query, "limit": limit},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = str(input_data.get("query", "")).strip() or "general"
        limit = int(input_data.get("limit", 5))
        self.log.info("檢索: %s", query)
        results = self._search(query, limit)
        summary = {
            "query": query,
            "result_count": len(results),
            "results": results,
        }
        return {"result": json.dumps(summary, ensure_ascii=False), "data": summary}
