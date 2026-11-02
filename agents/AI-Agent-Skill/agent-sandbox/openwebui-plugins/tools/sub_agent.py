"""
title: Sub Agent Tool
author: Skyzi000
description: 委托任務給子代理，保持主對話乾淨
version: 1.0.0
"""
from typing import Optional
import requests
class Tools:
    def __init__(self):
        self.sub_agent_endpoint = "http://localhost:8081/api/chat/completions"
    def delegate_task(self, task: str, agent_type: str = "coding") -> str:
        payload = {"model": f"sub-agent-{agent_type}", "messages": [{"role": "user", "content": task}], "stream": False}
        try:
            r = requests.post(self.sub_agent_endpoint, json=payload)
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"
