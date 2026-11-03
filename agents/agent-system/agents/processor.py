"""
ProcessorAgent — 資料清洗與格式轉化 Agent。

安全：處理結果預設執行 redact（遮罩 secret 樣式），
避免把檢索到的敏感資訊帶入後續流程或 log。
"""
import json
import re
from typing import Any, Dict

from agents.base_agent import BaseAgent, redact_text


class ProcessorAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("processor", **kwargs)

    @staticmethod
    def _clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
        return text.strip()

    @staticmethod
    def _strip_secrets(text: str) -> str:
        # 移除疑似憑證/金鑰片段，避免下游寫入檔案
        text = re.sub(r"sk-[A-Za-z0-9_-]{12,}", "***KEY***", text)
        text = re.sub(r"ghp_[A-Za-z0-9]{12,}", "***TOKEN***", text)
        text = re.sub(r"alv2_[A-Za-z0-9_-]{12,}", "***KEY***", text)
        text = re.sub(r"nvapi-[A-Za-z0-9_-]{12,}", "***KEY***", text)
        text = re.sub(r"\d{6,}:[A-Za-z0-9_-]{12,}", "***BOT_TOKEN***", text)
        return text

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raw = input_data.get("raw", "")
        mode = input_data.get("mode", "text")
        if isinstance(raw, list):
            raw = json.dumps(raw, ensure_ascii=False)
        raw = str(raw)
        cleaned = self._clean_text(raw)
        cleaned = self._strip_secrets(cleaned)
        cleaned = redact_text(cleaned)
        out = {
            "cleaned": cleaned,
            "char_count": len(cleaned),
            "mode": mode,
        }
        return {"result": json.dumps(out, ensure_ascii=False), "data": out}
