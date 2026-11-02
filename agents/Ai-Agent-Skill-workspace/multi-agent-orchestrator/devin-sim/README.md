# Devin 2.2 模擬接口（devin-sim）

Devin 是封閉雲端服務（無開放 CLI）。本目錄提供**等價模擬接口**：
以 OpenAI Agents SDK + LiteLLM 閘道重現 Devin 的「規劃 → 執行 → 自我驗證 → 回報」循環。

## 使用
```bash
# 模型直接執行
/root/ai-company/.venv/bin/python /root/AI-Agent-Skill/multi-agent-orchestrator/devin-sim/devin_sim.py "為 CRM 系統寫 API spec"

# 委派實際 CLI agent 執行
DELEGATE_TO=opencode /root/ai-company/.venv/bin/python .../devin_sim.py "修復 login bug"

# 指定模型
LLM_MODEL=nvidia/meta/llama-3.1-8b-instruct .../devin_sim.py "任務"
```

## 環境變數
| 變數 | 預設 | 說明 |
|---|---|---|
| LLM_BASE | `http://127.0.0.1:4000/v1` | LiteLLM 閘道 |
| LLM_MODEL | `glm-5.2` | 模型名 |
| LLM_API_KEY | `sk-dummy-litellm` | 閘道金鑰 |
| DELEGATE_TO | 空 | 執行層委派（opencode/aider/sweagent...） |

## 角色定位（多 agent 編排）
- **規劃**：產出可執行步驟
- **執行**：直接呼叫模型，或委派 opencode/aider/sweagent
- **驗證**：總結成果與風險（不假裝成功）
- 與 n8n 排程 + freebuff-daemon 心跳整合，可做為夜間自動任務的 Devin 角色
