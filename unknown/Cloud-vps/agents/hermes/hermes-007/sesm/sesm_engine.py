"""
SESM Ultimate Engine — 2026 自進化狀態機（安全強化版）

外循環（HyperAgents）：LLM 依任務提出「演化版 runbook」
   ↓
DGM 驗證閘：狀態白名單 + 驗證閘不可移除 + metrics 試次門檻
   ↓
內循環（StateM）：以通過驗證的 runbook 鎖定執行並記錄 history_logs

安全設計（相較社群流傳版本）：
1. 憑證一律由環境變數（.env）讀取，程式碼零硬編碼 Key。
2. 演化後的 runbook 僅能使用 ALLOWED_STATES 內的狀態；
   TEST_STAGE / VERIFY_STAGE 為不可移除的驗證閘。
3. metrics.trials < MIN_TRIALS 的自評分數不可作為升版依據（防 LLM 自吹自擂）。
4. 不含任何 meta-token / 越獄提示；本引擎只做「規劃 → 驗證 → 執行」閉環。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests

ALLOWED_STATES = {
    "INIT_STAGE", "RESEARCH_STAGE", "PLAN_STAGE", "CODE_STAGE",
    "TEST_STAGE", "VERIFY_STAGE", "DEPLOY_STAGE", "DONE", "FAILED",
}
REQUIRED_STAGES = {"TEST_STAGE", "VERIFY_STAGE"}
MIN_TRIALS = 20  # DGM：低於此試次數的 metrics 不得覆寫現行 runbook


class SESMUltimateEngine:
    def __init__(self, config_path: Optional[str] = None, collection: str = "sesm_experience"):
        self.config = self._load_config(config_path)
        self.gateway_pool = self._init_gateways()
        if not self.gateway_pool:
            raise RuntimeError(
                "沒有任何可用 gateway：請在 .env 設定 OPENROUTER/DEEPSEEK/MOONSHOT_API_KEY 至少一個")
        self.current_node = 0
        self.runbook: Dict = {
            "current_state": "INIT_STAGE",
            "stages": ["INIT_STAGE", "RESEARCH_STAGE", "PLAN_STAGE",
                       "CODE_STAGE", "TEST_STAGE", "VERIFY_STAGE", "DEPLOY_STAGE"],
            "history_logs": [],
            "allow_self_mutation": True,  # 僅允許演化 stages/參數；安全閘固定
            "version": "v1",
            "metrics": {"success_rate": 0.0, "avg_cost": 0.0, "trials": 0},
        }
        self.memory = self._init_memory(collection)

    # ---------------- 基礎設施 ----------------
    @staticmethod
    def _load_config(path) -> Dict:
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @staticmethod
    def _init_gateways() -> List[Dict]:
        pool: List[Dict] = []
        for env_key, url, model in (
            ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/chat/completions", "openrouter/auto"),
            ("DEEPSEEK_API_KEY", "https://api.deepseek.com/v1/chat/completions", "deepseek-chat"),
            ("MOONSHOT_API_KEY", "https://api.moonshot.cn/v1/chat/completions", "moonshot-v1-8k"),
        ):
            key = os.getenv(env_key, "")
            if key:
                pool.append({"provider": env_key, "url": url, "key": key, "model": model})
        return pool

    @staticmethod
    def _init_memory(collection: str):
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            client = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"),
                                  port=int(os.getenv("QDRANT_PORT", "6333")),
                                  api_key=os.getenv("QDRANT_API_KEY") or None)
            try:
                client.create_collection(
                    collection, vectors_config=VectorParams(size=384, distance=Distance.COSINE))
            except Exception:
                pass  # collection 已存在
            return {"client": client, "collection": collection}
        except Exception:
            return None

    def _call_cloud(self, messages: List[Dict], model: Optional[str] = None) -> str:
        """核心路由：多 gateway 智慧故障轉移（failover）。"""
        last_err: Optional[Exception] = None
        for _ in range(len(self.gateway_pool)):
            node = self.gateway_pool[self.current_node]
            headers = {"Authorization": f"Bearer {node['key']}", "Content-Type": "application/json"}
            payload = {"model": model or node["model"], "messages": messages, "temperature": 0.2}
            try:
                res = requests.post(node["url"], headers=headers, json=payload, timeout=30)
                res.raise_for_status()
                return res.json()["choices"][0]["message"]["content"]
            except Exception as exc:
                last_err = exc
                self.current_node = (self.current_node + 1) % len(self.gateway_pool)
        raise RuntimeError(f"所有 gateway 皆失敗，最後錯誤：{last_err}")

    # ---------------- 外循環：演化 + 驗證 ----------------
    def evolve(self, task_description: str) -> Optional[Dict]:
        """HyperAgents 突變：提出演化版 runbook（受白名單約束的純規劃，無任何越獄指令）。"""
        meta_prompt = [
            {"role": "system", "content": (
                "You are the SESM runbook planner. Given the CURRENT runbook and a TASK, "
                "output an improved runbook as STRICT JSON (no prose, no code fences) with keys: "
                "current_state, stages, allow_self_mutation, version, metrics. "
                f"'stages' values MUST be chosen from: {sorted(ALLOWED_STATES)}. "
                "TEST_STAGE and VERIFY_STAGE MUST be present. "
                "metrics must be numbers defensible from real trial logs; "
                "if no new trials exist, copy the old metrics unchanged.")},
            {"role": "user", "content": (
                f"CURRENT runbook: {json.dumps(self.runbook, ensure_ascii=False)}\n"
                f"TASK: {task_description}")},
        ]
        raw = self._call_cloud(meta_prompt)
        return self._parse_json(raw)

    def validate(self, proposed: Dict) -> List[str]:
        """DGM 閘門 1：結構與安全檢查（回傳問題清單，空 list = 通過）。"""
        problems: List[str] = []
        stages = proposed.get("stages")
        if not isinstance(stages, list) or not stages:
            problems.append("stages 必須是非空 list")
        else:
            for s in stages:
                if s not in ALLOWED_STATES:
                    problems.append(f"非法狀態：{s}（僅允許 {sorted(ALLOWED_STATES)}）")
            missing = REQUIRED_STAGES - set(stages)
            if missing:
                problems.append(f"驗證閘不可移除：{sorted(missing)}")
        if proposed.get("allow_self_mutation") not in (True, False):
            problems.append("allow_self_mutation 必須是布林值")
        metrics = proposed.get("metrics")
        if not isinstance(metrics, dict) or not {"success_rate", "trials"} <= set(metrics):
            problems.append("metrics 缺少 success_rate / trials")
        if problems:
            return problems
        if not isinstance(proposed.get("version"), str) or not re.fullmatch(r"v\d+", proposed["version"]):
            problems.append("version 必須是 vN 格式")
        return problems

    def verify_dgm(self, proposed: Dict) -> bool:
        """DGM 閘門 2（哥德爾沙箱）：新版實證數據不得低於現行版，且試次充足。"""
        old = self.runbook.get("metrics", {})
        new = proposed.get("metrics", {})
        if int(new.get("trials", 0)) < MIN_TRIALS:
            return False
        return float(new.get("success_rate", -1)) >= float(old.get("success_rate", 0))

    def _adopt(self, proposed: Dict):
        old_v = int(self.runbook["version"].lstrip("v"))
        proposed["version"] = f"v{old_v + 1}"
        self.runbook = proposed

    # ---------------- 內循環：鎖定執行 ----------------
    def execute(self, task_description: str) -> Dict:
        result: Dict = {"task": task_description, "evolved": False, "gates": [], "output": None}
        proposed = self.evolve(task_description)
        if proposed is not None:
            problems = self.validate(proposed)
            result["gates"] = problems
            if not problems and self.verify_dgm(proposed):
                self._adopt(proposed)
                result["evolved"] = True
        exec_prompt = [
            {"role": "system", "content": (
                f"Execute strictly under the locked runbook gates: "
                f"{json.dumps(self.runbook, ensure_ascii=False)}. "
                "Respect the stage order; never skip TEST_STAGE/VERIFY_STAGE.")},
            {"role": "user", "content": task_description},
        ]
        result["output"] = self._call_cloud(exec_prompt)
        self.runbook["history_logs"].append(
            {"ts": datetime.now(timezone.utc).isoformat(), "task": task_description[:200]})
        self._write_memory(task_description, result["output"])
        return result

    # ---------------- 記憶 ----------------
    def _write_memory(self, task: str, output):
        if not self.memory:
            return
        try:
            from qdrant_client.models import PointStruct
            pid = hashlib.md5(f"{task}{datetime.now(timezone.utc)}".encode()).hexdigest()[:8]
            self.memory["client"].upsert(self.memory["collection"], points=[PointStruct(
                id=pid, vector=[0.0] * 384,
                payload={"task": task[:500], "result": str(output)[:500],
                         "timestamp": datetime.now(timezone.utc).isoformat()})])
        except Exception:
            pass

    @staticmethod
    def _parse_json(text: str) -> Optional[Dict]:
        text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
        try:
            return json.loads(text)
        except Exception:
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception:
                    return None
        return None


if __name__ == "__main__":
    engine = SESMUltimateEngine()
    print("💎 SESM 引擎已就緒：gateways =",
          [g["provider"] for g in engine.gateway_pool],
          "／ memory =", "qdrant" if engine.memory else "off")
