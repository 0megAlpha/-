"""任務: 程式碼生成。"""
from typing import Any, Dict


def run(agent, inputs: Dict[str, Any]) -> Dict[str, Any]:
    plan = inputs.get("plan", "")
    if isinstance(plan, str):
        try:
            import json
            plan = json.loads(plan)
        except Exception:  # noqa: BLE001
            pass
    return agent.run({"plan": str(plan)[:2000], "language": "python", "filename": "generated_output.py"})
