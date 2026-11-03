"""
CoderAgent — 程式碼生成與修改 Agent。

安全：生成的程式碼只寫入 AGENT_WORKSPACE（預設 workflows/state/workspace，
已被 .gitignore 排除），且寫入前做 secret 遮罩；不觸碰 repo 內其他檔案。
"""
import os
import json
import re
from typing import Any, Dict

from agents.base_agent import BaseAgent, redact_text


class CoderAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("coder", **kwargs)
        default_ws = os.path.join(self.workdir, "workflows", "state", "workspace")
        self.workspace = os.getenv("AGENT_WORKSPACE", default_ws)
        os.makedirs(self.workspace, exist_ok=True)

    def _sanitize_code(self, code: str) -> str:
        code = redact_text(code)
        # 移除被偵測到的金鑰賦值行
        code = re.sub(r"(?im)^(\s*(?:api_key|token|password|secret)\s*=\s*)[\"'][^\"']+[\"']", r"\1'***'", code)
        return code

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        plan = input_data.get("plan", "")
        language = input_data.get("language", "python")
        filename = input_data.get("filename", "generated_output.py")
        prompt = (
            f"請依照以下計劃，產出 {language} 程式碼。只輸出程式碼，不要解釋。\n"
            f"計劃: {str(plan)[:2000]}"
        )
        raw = self.call_llm([{"role": "user", "content": prompt}], temperature=0.2)
        if self.mock:
            raw = "# mock 產出\nprint('hello from coder agent')\n"
        code = self._sanitize_code(raw)
        # 只允許安全檔名（避免路徑穿越）
        safe_name = os.path.basename(filename or "generated_output.py")
        out_path = os.path.join(self.workspace, safe_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code)
        return {"result": out_path, "data": {"path": out_path, "chars": len(code)}}
