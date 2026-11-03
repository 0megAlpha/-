"""
NotifierAgent — Telegram 通知 Agent。

安全：bot token 與 chat id 一律從環境變數讀取（TELEGRAM_BOT_TOKEN /
TELEGRAM_CHAT_ID），mock 或佔位符時僅 log 不發送。
"""
import os
import json
from typing import Any, Dict

from agents.base_agent import BaseAgent


class NotifierAgent(BaseAgent):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("notifier", **kwargs)
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID_HERE")

    def _send(self, text: str) -> bool:
        if self.mock or self.bot_token.startswith("YOUR_") or self.chat_id.startswith("YOUR_"):
            self.log.info("[mock] 通知略過: %s", text[:80])
            return True
        import requests
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        resp = requests.post(url, data={"chat_id": self.chat_id, "text": text}, timeout=30)
        return resp.status_code == 200

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        summary = str(input_data.get("summary", ""))[:3500]
        title = str(input_data.get("title", "Agent 工作流完成"))
        message = f"{title}\n{summary}"
        ok = self._send(message)
        return {"result": "sent" if ok else "failed", "data": {"ok": ok}}
