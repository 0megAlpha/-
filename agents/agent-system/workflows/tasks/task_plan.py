"""任務: 規劃拆解。"""
from typing import Any, Dict


def run(agent, inputs: Dict[str, Any]) -> Dict[str, Any]:
    return agent.run({"context": inputs.get("context", ""), "objective": inputs.get("objective", "完成任務")})
