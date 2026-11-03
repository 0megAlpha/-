"""
MemoryAgent — 記憶與狀態管理 Agent。

儲存位置：workflows/state/memory.json（已被 .gitignore 排除），
提供 set / get / list / clear 操作。
"""
import os
import json
import time
from typing import Any, Dict

from agents.base_agent import BaseAgent


class MemoryAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("memory", **kwargs)
        default_path = os.path.join(self.workdir, "workflows", "state", "memory.json")
        self.store_path = os.getenv("MEMORY_STORE_PATH", default_path)
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        self._data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.store_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:  # noqa: BLE001
            return {}

    def _persist(self) -> None:
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action", "get")
        key = str(input_data.get("key", ""))
        if action == "set" and key:
            self._data[key] = {
                "value": input_data.get("value"),
                "updated_at": time.strftime("%F %T"),
            }
            self._persist()
            return {"result": "saved", "data": {"key": key}}
        if action == "clear":
            self._data.clear()
            self._persist()
            return {"result": "cleared", "data": {}}
        if action == "list":
            return {"result": json.dumps(list(self._data.keys()), ensure_ascii=False),
                    "data": {"keys": list(self._data.keys())}}
        return {"result": json.dumps(self._data.get(key), ensure_ascii=False), "data": self._data.get(key)}
