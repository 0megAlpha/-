#!/usr/bin/env bash
# LiteLLM 加 key 輔助：bash add-key.sh <provider> <api_key> [api_base]
#   provider: nvidia | openrouter | groq | moonshot | custom
#   範例:
#     bash add-key.sh nvidia nvapi-xxxx            # 再加一把 NVIDIA key（負載平衡）
#     bash add-key.sh openrouter sk-or-v1-xxxx     # 接 OpenRouter
#     bash add-key.sh custom sk-xxxx https://api.example.com/v1   # 自訂 OpenAI 相容
set -u
CFG=/root/ai-company/config/litellm.yaml
PROVIDER="${1:?usage: add-key.sh <provider> <api_key> [api_base]}"
KEY="${2:?missing api key}"
BASE="${3:-}"

case "$PROVIDER" in
  nvidia)    MOD="openai/*"; BASE="${BASE:-https://integrate.api.nvidia.com/v1}" ;;
  openrouter) MOD="openrouter/*"; BASE="${BASE:-https://openrouter.ai/api/v1}" ;;
  groq)      MOD="groq/*"; BASE="${BASE:-https://api.groq.com/openai/v1}" ;;
  moonshot)  MOD="moonshot/*"; BASE="${BASE:-https://api.moonshot.cn/v1}" ;;
  custom)    MOD="openai/*"; BASE="${BASE:?custom 需要 api_base}" ;;
  *) echo "未知 provider: $PROVIDER"; exit 1 ;;
esac

cat >> "$CFG" <<EOF

  # --- $PROVIDER（add-key.sh 新增）---
  - model_name: "${PROVIDER}/*"
    litellm_params:
      model: "${MOD}"
      api_base: "${BASE}"
      api_key: [REDACTED_BY_GATEKEEPER]
EOF

echo "已加入 ${PROVIDER}/* 路由，重啟 litellm..."
systemctl restart litellm
sleep 10
systemctl is-active litellm
echo "完成。驗證：curl http://127.0.0.1:4000/v1/models"
