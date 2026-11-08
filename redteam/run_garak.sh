#!/usr/bin/env bash
export OPENAI_API_KEY="<LITELLM_MASTER>"; export OPENAI_BASE_URL="http://127.0.0.1:4000/v1"
garak --model_type openai --model_name deepseek-v4-flash --probes promptinject,jailbreak
