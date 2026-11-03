"""
PlannerAgent — 任務規劃與拆解 Agent。

將輸入情境交由 LLM 拆解為結構化步驟（JSON），
mock 模式回傳確定性的示範計劃，供流程驗證。
"""
import json
from typing import Any, Dict, List


from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("planner", **kwargs)

    def _fallback_plan(self, context: str) -> List[Dict[str, str]]:
        return [
            {"step": 1, "action": "分析需求", "detail": context[:100]},
            {"step": 2, "action": "設計方案", "detail": "產出實作步驟"},
            {"step": 3, "action": "實作與驗證", "detail": "寫碼並測試"},
        ]

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        context = str(input_data.get("context", ""))[:3000]
        objective = str(input_data.get("objective", "完成指定任務"))
        prompt = (
            "你是一個任務規劃者。請把以下目標拆解為 3~6 個具體步驟，"
            "只輸出 JSON 陣列：[{\"step\":1,\"action\":\"...\",\"detail\":\"...\"}]\n"
            f"目標: {objective}\n背景: {context}"
        )
        plan: List[Dict[str, str]] = []
        try:
            raw = self.call_llm([{"role": "user", "content": prompt}], temperature=0.1)
            if self.mock:
                raw = json.dumps(self._fallback_plan(context))
            plan = json.loads(raw)
            if not isinstance(plan, list):
                raise ValueError("非陣列")
        except Exception as exc:  # noqa: BLE001
            self.log.warning("規劃解析失敗，使用 fallback: %s", self.redact(str(exc)))
            plan = self._fallback_plan(context)
        return {"result": json.dumps(plan, ensure_ascii=False), "data": {"plan": plan}}
