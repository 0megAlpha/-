# OpenHands 部署说明

1. 启动 LiteLLM：
   bash litellm/start.sh

2. 载入环境：
   export OPENAI_API_BASE="http://127.0.0.1:4000/v1"
   export OPENAI_API_KEY="sk-anything"
   export OH_MODEL="litellm_proxy/pollinations-free"
   export OH_BASE_URL="http://127.0.0.1:4000"
   export OH_API_KEY="sk-anything"

3. 启动：
   openhands
