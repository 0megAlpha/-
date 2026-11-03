"""
BaseAgent — 所有 Agent 的基礎類別。

安全規範（強制）：
1. 所有敏感參數一律透過環境變數讀取（os.getenv），嚴禁 hardcode。
2. 預設值只允許 localhost / 127.0.0.1 / 佔位符（YOUR_*_HERE）。
3. 日誌與輸出一律經過 redact() 遮罩，永不寫入真實金鑰。
4. MOCK_LLM=1 或金鑰仍為佔位符時，進入 mock 模式（不需真實 API 即可驗證流程）。
"""
import os
import json
import time
import logging
from typing import Any, Dict, List, Optional

# 變數名稱含這些關鍵字時，redact 會遮罩其值
_SECRET_KEYWORDS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD", "AUTH", "CREDENTIAL")


def _is_secret_name(name: str) -> bool:
    up = name.upper()
    return any(k in up for k in _SECRET_KEYWORDS)


def redact_text(text: str) -> str:
    """遮罩常見 secret 樣式（sk- / token 等），避免誤寫入 log。"""
    import re
    text = re.sub(r"(sk-[A-Za-z0-9]{4})[A-Za-z0-9_-]+", r"\1***", text)
    text = re.sub(r"(nvapi-[A-Za-z0-9]{4})[A-Za-z0-9_-]+", r"\1***", text)
    text = re.sub(r"(alv2_[A-Za-z0-9]{4})[A-Za-z0-9_-]+", r"\1***", text)
    text = re.sub(r"(ghp_[A-Za-z0-9]{4})[A-Za-z0-9_-]*", r"\1***", text)
    text = re.sub(r"(github_pat_[A-Za-z0-9_]{4})[A-Za-z0-9_]*", r"\1***", text)
    text = re.sub(r"(\d{6,}:[A-Za-z0-9_-]{6,})", "***BOT_TOKEN***", text)
    return text


class BaseAgent:
    def __init__(self, agent_name: str, **kwargs: Any) -> None:
        self.agent_name = agent_name
        # 一律從環境變數讀取（僅允許 localhost 預設）
        self.llm_base_url = os.getenv("LITELLM_BASE_URL", "http://localhost:4000/v1")
        self.api_key = os.getenv("LITELLM_MASTER_KEY", "YOUR_LITELLM_MASTER_KEY_HERE")
        self.llm_model = os.getenv("LITELLM_MODEL", "openai/glm-5.2")
        self.llm_timeout = int(os.getenv("LLM_TIMEOUT", "120"))
        self.mock = os.getenv("MOCK_LLM", "0") == "1"
        self.mock = self.mock or self.api_key.startswith("YOUR_") or not self.api_key
        self.workdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.log = logging.getLogger(f"agent.{agent_name}")
        self._ensure_logging()

    # ───────── 基礎工具 ─────────
    def _ensure_logging(self) -> None:
        if not logging.getLogger().handlers:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
        if self.log.level == logging.NOTSET:
            self.log.setLevel(logging.INFO)

    def redact(self, text: str) -> str:
        """遮罩可能的 secret 後回傳，用於 log。"""
        return redact_text(str(text))

    def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.2,
                 max_tokens: int = 2048) -> str:
        """
        呼叫 OpenAI 相容端點（LiteLLM）。
        mock 模式下不發網路請求，回傳模擬結果 — 讓流程無金鑰也能驗證。
        """
        if self.mock:
            prompt = messages[-1].get("content", "") if messages else ""
            self.log.info("[mock] LLM 呼叫略過（MOCK_LLM=1 或金鑰為佔位符）")
            return json.dumps(
                {"mock": True, "agent": self.agent_name,
                 "echo": prompt[:120]},
                ensure_ascii=False,
            )
        import requests  # 延遲匯入，保持依賴輕量
        payload = {
            "model": self.llm_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        url = f"{self.llm_base_url.rstrip('/')}/chat/completions"
        self.log.info("LLM 呼叫 %s (model=%s)", url, self.llm_model)
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.llm_timeout)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            self.log.error("LLM 呼叫失敗: %s", self.redact(str(exc)))
            raise

    def load_json(self, path: str) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, path: str, data: Any) -> str:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    # ───────── 核心介面 ─────────
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """所有子類別 Agent 必須實現的核心執行方法。"""
        raise NotImplementedError("Subclasses must implement execute method.")

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """執行包裝：計時、log 輸入輸出（redact）、回傳結果。"""
        started = time.time()
        self.log.info("[%s] 開始, input_keys=%s", self.agent_name, sorted(input_data.keys()))
        result = self.execute(input_data)
        elapsed = round(time.time() - started, 3)
        self.log.info("[%s] 完成, elapsed=%ss, result_keys=%s",
                      self.agent_name, elapsed, sorted(result.keys()) if isinstance(result, dict) else type(result).__name__)
        result["_meta"] = {"agent": self.agent_name, "elapsed_s": elapsed}
        return result
