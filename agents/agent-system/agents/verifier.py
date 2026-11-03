"""
VerifierAgent — 驗證與測試執行 Agent。

安全：只允許執行 VERIFY_ALLOWED_COMMANDS 白名單內的指令（環境變數設定），
預設僅允許無害指令；輸出不做回傳以免洩漏。
"""
import os
import json
import shlex
import subprocess
from typing import Any, Dict

from agents.base_agent import BaseAgent


class VerifierAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("verifier", **kwargs)
        allowed = os.getenv("VERIFY_ALLOWED_COMMANDS", "python3 --version,true")
        self.allowed_cmds = {c.strip() for c in allowed.split(",") if c.strip()}

    def _run(self, cmd: str, timeout: int = 30) -> Dict[str, Any]:
        args = shlex.split(cmd)
        if not args or args[0] not in self.allowed_cmds:
            return {"ok": False, "error": "指令不在白名單"}
        try:
            proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
            return {"ok": proc.returncode == 0, "exit_code": proc.returncode}
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "timeout"}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc)}

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        artifact = str(input_data.get("artifact", ""))
        cmd = str(input_data.get("command", "")).strip()
        if not cmd:
            cmd = "python3 --version"
        result = self._run(cmd)
        result["artifact"] = artifact
        return {"result": json.dumps(result, ensure_ascii=False), "data": result}
