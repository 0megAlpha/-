"""任務: 研究檢索。"""
from typing import Any, Dict


def run(agent, inputs: Dict[str, Any]) -> Dict[str, Any]:
    return agent.run({"query": inputs.get("query", ""), "limit": inputs.get("limit", 5)})
