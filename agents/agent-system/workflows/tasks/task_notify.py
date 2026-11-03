"""任務: 通知。"""
import json
from typing import Any, Dict


def run(agent, inputs: Dict[str, Any]) -> Dict[str, Any]:
    summary = inputs.get("summary", "")
    if isinstance(summary, str):
        try:
            data = json.loads(summary)
            summary = json.dumps(data.get("data", data), ensure_ascii=False)[:2000]
        except Exception:  # noqa: BLE001
            pass
    return agent.run({"summary": str(summary), "title": "Agent 工作流完成"})
