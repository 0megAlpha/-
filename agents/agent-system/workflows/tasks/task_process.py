"""任務: 資料清洗。"""
import json
from typing import Any, Dict


def run(agent, inputs: Dict[str, Any]) -> Dict[str, Any]:
    raw = inputs.get("raw", "")
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
            raw = json.dumps(data, ensure_ascii=False)
        except Exception:  # noqa: BLE001
            pass
    return agent.run({"raw": raw, "mode": "pipeline"})
