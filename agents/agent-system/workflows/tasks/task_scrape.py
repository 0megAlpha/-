"""任務: 網頁抓取。"""
import json
from typing import Any, Dict


def run(agent, inputs: Dict[str, Any]) -> Dict[str, Any]:
    raw = inputs.get("query", "")
    urls = []
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
            urls = [r.get("url") for r in data.get("results", []) if r.get("url")]
        except Exception:  # noqa: BLE001
            pass
    return agent.run({"urls": urls, "raw": raw})
