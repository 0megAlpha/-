#!/bin/bash

# =========================================================
# 讀取傳入的金鑰清單並自動分類測試
# =========================================================

# 請將你的 金鑰清單 存放在 keys.txt，或直接寫在陣列中
KEYS_INPUT='
AIzaSyB-abc123def456ghi789jklmno012345
AKIAREDACTED
AKIAREDACTED
ghp_REDACTED
ghp_REDACTED
ghp_REDACTED
ghp_REDACTED
ghp_REDACTED
ghp_REDACTED
nvapi-TEST-KEY-PLACEHOLDER-000000000000000000000000
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
sk-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
xox-REDACTED
'

echo "=================================================="
echo "          開始執行 Key 自動辨識與測試腳本        "
echo "=================================================="

# 設定本地 API Gateway 備用網址 (如果有的話)
LOCAL_GATEWAY="http://localhost:4000/v1"

echo "$KEYS_INPUT" | while read -r key; do
  # 略過空行
  [[ -z "$key" ]] && continue
  
  # 去除空格與引號
  key=$(echo "$key" | xargs | tr -d "'\"")

  # 1. 根據 Key 前綴判斷服務商類型與 Endpoint
  if [[ "$key" == AIzaSy* ]]; then
    provider="Google Gemini"
    endpoint="https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    model="gemini-1.5-flash"
    auth_header="Authorization: Bearer $key"

  elif [[ "$key" == nvapi-* ]]; then
    provider="NVIDIA NIM"
    endpoint="https://integrate.api.nvidia.com/v1/chat/completions"
    model="meta/llama-3.1-8b-instruct"
    auth_header="Authorization: Bearer $key"

  elif [[ "$key" == sk-or-v1-* || "$key" == sk-or-* ]]; then
    provider="OpenRouter"
    endpoint="https://openrouter.ai/api/v1/chat/completions"
    model="google/gemini-flash-1.5"
    auth_header="Authorization: Bearer $key"

  elif [[ "$key" == sk-ant-* ]]; then
    provider="Anthropic (Claude)"
    endpoint="https://api.anthropic.com/v1/messages"
    model="claude-3-haiku-20240307"
    # Claude 原生格式特殊處理
    auth_header="x-api-key: $key"

  elif [[ "$key" == ghp_* || "$key" == github_pat_* ]]; then
    provider="GitHub Models"
    endpoint="https://models.inference.ai.azure.com/chat/completions"
    model="gpt-4o-mini"
    auth_header="Authorization: Bearer $key"

  elif [[ "$key" == AKIA* ]]; then
    provider="AWS Access Key"
    endpoint="N/A (AWS IAM Key，非 LLM API Key)"
    echo -e "測試 Key: ${key:0:12}... | 類型: \033[33m$provider\033[0m | \033[31m[跳過 - 非 LLM Key]\033[0m"
    continue

  elif [[ "$key" == xoxb-* ]]; then
    provider="Slack Bot Token"
    endpoint="N/A (Slack Bot Token)"
    echo -e "測試 Key: ${key:0:12}... | 類型: \033[33m$provider\033[0m | \033[31m[跳過 - 非 LLM Key]\033[0m"
    continue

  elif [[ "$key" == sk-proj-* || "$key" == sk-* ]]; then
    # 一般 OpenAI 格式或自建中轉/偽造 Key
    provider="OpenAI / 中轉門戶"
    endpoint="https://api.openai.com/v1/chat/completions"
    model="gpt-4o-mini"
    auth_header="Authorization: Bearer $key"

  else
    provider="未知格式 / 本地測試"
    endpoint="${LOCAL_GATEWAY}/chat/completions"
    model="auto"
    auth_header="Authorization: Bearer $key"
  fi

  # 顯示測試進度 (僅顯示 Key 的前幾碼遮罩)
  masked_key="${key:0:10}...${key:-4}"
  echo -n "測試: [$masked_key] ($provider) -> "

  # 針對 Anthropic 發送特殊 Payload，其餘發送 OpenAI 相容格式
  if [[ "$provider" == "Anthropic (Claude)" ]]; then
    response=$(curl -s -w "\n%{http_code}" --max-time 4 -X POST "$endpoint" \
      -H "$auth_header" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d "{
        \"model\": \"$model\",
        \"max_tokens\": 5,
        \"messages\": [{\"role\": \"user\", \"content\": \"hi\"}]
      }")
  else
    response=$(curl -s -w "\n%{http_code}" --max-time 4 -X POST "$endpoint" \
      -H "$auth_header" \
      -H "Content-Type: application/json" \
      -d "{
        \"model\": \"$model\",
        \"messages\": [{\"role\": \"user\", \"content\": \"hi\"}],
        \"max_tokens\": 5
      }")
  fi

  http_code=$(echo "$response" | tail -n1)

  if [ "$http_code" -eq 200 ]; then
    echo -e "\033[32m[成功 200 OK]\033[0m"
  elif [ "$http_code" -eq 401 ]; then
    echo -e "\033[31m[失敗 401 無效Key/未授權]\033[0m"
  elif [ "$http_code" -eq 404 ]; then
    echo -e "\033[33m[404 端點或模型不存在]\033[0m"
  else
    echo -e "\033[31m[失敗 HTTP $http_code]\033[0m"
  fi

done

echo "=================================================="
echo "                    測試完成                      "
echo "=================================================="
