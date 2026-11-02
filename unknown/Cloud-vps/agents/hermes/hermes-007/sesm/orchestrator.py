"""
AI Company Orchestrator — CEO → Hermes → Agent Fleet → Verification

LangGraph 未安裝時可獨立運行；安裝後可將 run() 嫁接成 StateGraph 節點
（Hermes 規劃 → 選 Agent → 派發 → 驗證 → 回寫 Memory）。
"""
from __future__ import annotations

import json
import os
from typing import Dict, Optional

import requests


class AICompanyOrchestrator:
    def __init__(self, registry_path: Optional[str] = None):
        self.hermes_url = os.getenv("HERMES_API_URL", "http://localhost:8642")
        self.hermes_key = os.getenv("HERMES_API_KEY", "")
        self.registry_path = registry_path or os.path.join(
            os.path.dirname(__file__), "agent_registry.json")
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        if os.path.exists(self.registry_path):
            with open(self.registry_path, encoding="utf-8") as f:
                return json.load(f)
        return {"agents": [], "selection_rules": {}}

    # ---------------- Hermes 規劃 ----------------
    def call_hermes(self, goal: str) -> Dict:
        headers = {"Authorization": f"Bearer {self.hermes_key}",
                   "Content-Type": "application/json"}
        payload = {"messages": [{"role": "user",
                                 "content": f"Plan this goal and return a task list: {goal}"}]}
        try:
            res = requests.post(f"{self.hermes_url}/v1/chat/completions",
                                headers=headers, json=payload, timeout=60)
            res.raise_for_status()
            return res.json()
        except Exception as exc:
            return {"error": str(exc)}

    # ---------------- Agent 選擇與派發 ----------------
    def select_agent(self, task: Dict) -> str:
        rules = self.registry.get("selection_rules", {})
        return rules.get(task.get("type", "日常編碼"), "opencode")

    def dispatch(self, task: Dict, agent: str) -> Dict:
        endpoints = {
            "openhands": os.getenv("OPENHANDS_ENDPOINT", "http://localhost:18000"),
            "opencode": os.getenv("OPENCODE_ENDPOINT", "http://localhost:8743"),
        }
        endpoint = endpoints.get(agent)
        if not endpoint:
            return {"status": "skipped",
                    "reason": f"agent {agent} 尚無 dispatch endpoint（請由 Hermes 透過 MCP/CLI 派發）"}
        try:
            res = requests.post(f"{endpoint}/task", json=task, timeout=300)
            res.raise_for_status()
            return res.json()
        except Exception as exc:
            return {"status": "failed", "error": str(exc)}

    # ---------------- 主流程 ----------------
    def run(self, goal: str) -> Dict:
        state: Dict = {"goal": goal, "iteration": 0}
        plan = self.call_hermes(goal)
        state["plan"] = plan
        tasks = plan.get("tasks") if isinstance(plan, dict) else None
        if not tasks:
            # Hermes 未回覆時的安全降級：不讓流程卡死
            tasks = [{"type": "日常編碼", "description": goal}]
        state["tasks"] = tasks
        assignments = []
        for task in tasks:
            agent = self.select_agent(task)
            assignments.append({"task": task, "agent": agent,
                                "result": self.dispatch(task, agent)})
        state["agent_assignments"] = assignments
        # TODO（下一階段）: Verification 節點 + Hermes 回寫 engineering-memory
        return state


if __name__ == "__main__":
    orch = AICompanyOrchestrator()
    print("🎯 Orchestrator 已就緒：agents =",
          [a["name"] for a in orch.registry.get("agents", [])])
