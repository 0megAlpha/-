#!/usr/bin/env python3
"""
Devin 2.2 模擬接口（devin-sim）
================================
以 OpenAI Agents SDK 實作的 Devin 工作模式模擬：
接收任務 -> 規劃 -> 執行（呼叫 LiteLLM 閘道模型）-> 驗證 -> 回報。

Devin 本身是封閉雲端服務，本模擬器提供等價的
「規劃 - 執行 - 自我驗證 - 回報」介面，可作為多 agent 編排中的 Devin 角色。

用法:
  /root/ai-company/.venv/bin/python devin_sim.py "建立一個 REST API 的 spec"
  DELEGATE_TO="opencode" ...  # 執行層委派（opencode / aider / sweagent）
"""

import json
import os
import subprocess
import sys
import time

TASK = sys.argv[1] if len(sys.argv) > 1 else "Explain what you can do"
DELEGATE = os.environ.get("DELEGATE_TO", "").strip()

LLM_BASE = os.environ.get("LLM_BASE", "http://127.0.0.1:4010/v1")  # 統一模擬 API
LLM_MODEL = os.environ.get("LLM_MODEL", "glm-5.2")

def _load_key():
    for p in ("/root/Google-ai/.sim-key", "/root/工作流部署/01-模擬API/.sim-key", "/root/AI-Agent-Skill/.sim-key"):
        try:
            k = open(p).read().strip()
            if k:
                return k
        except Exception:
            pass
    return os.environ.get("LLM_API_KEY", "")

LLM_KEY = os.environ.get("LLM_API_KEY") or _load_key()


def call_llm(system: str, user: str) -> str:
    """透過 LiteLLM 閘道呼叫模型（OpenAI 相容）。"""
    try:
        from openai import OpenAI
        client = OpenAI(base_url=LLM_BASE, api_key=LLM_KEY)
        resp = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:  # 閘道不可用時回退本機 ollama
        try:
            from openai import OpenAI as O2
            c2 = O2(base_url="http://127.0.0.1:11434/v1", api_key=[REDACTED_BY_GATEKEEPER])
            r2 = c2.chat.completions.create(
                model="qwen3:4b",
                messages=[{"role": "user", "content": system + "\n\n" + user}],
                temperature=0.3,
            )
            return r2.choices[0].message.content or ""
        except Exception:
            return f"[devin-sim] 模型閘道不可用: {e}"


def run(cmd: list, timeout: int = 300) -> tuple:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout[-2000:], p.stderr[-2000:]
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


def main():
    t0 = time.time()
    print(f"[devin-sim] 任務: {TASK}")
    print(f"[devin-sim] 執行層委派: {DELEGATE or '模型直接執行'}")

    # 1) 規劃
    plan = call_llm(
        "你是 Devin 規劃器。產出 step-by-step 執行計畫（簡短、可執行）。",
        TASK,
    )
    print("[devin-sim] 規劃完成:") 
    print(plan[:800])

    # 2) 執行（可選委派給實際 CLI agent）
    if DELEGATE:
        print(f"[devin-sim] 委派 {DELEGATE} 執行...")
        rc, out, err = run([DELEGATE, "run", TASK], timeout=600)
        print(f"[devin-sim] 委派 rc={rc}")
        if out:
            print(out[:1500])
        if rc != 0 and err:
            print("[devin-sim] stderr:", err[:800])

    # 3) 驗證摘要
    summary = call_llm(
        "你是 Devin 驗證員。總結成果與風險（3-5 點），不要假裝成功。",
        f"任務: {TASK}\n計畫: {plan[:1200]}",
    )
    print("[devin-sim] 驗證摘要:")
    print(summary[:800])
    print(f"[devin-sim] 完成，耗時 {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
