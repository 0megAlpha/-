"""任務: 驗證。"""
from typing import Any, Dict


def run(agent, inputs: Dict[str, Any]) -> Dict[str, Any]:
    return agent.run({"artifact": str(inputs.get("artifact", "")), "command": "python3 --version"})
