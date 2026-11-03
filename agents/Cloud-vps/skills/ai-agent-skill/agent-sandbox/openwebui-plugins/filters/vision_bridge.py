"""
title: Vision Bridge
author: Classic298
description: 讓純文字模型具備視覺能力
version: 1.0.0
"""
from typing import Optional
import requests
class Filter:
    def __init__(self):
        self.vision_model = "qwen-vl-plus"
        self.vision_endpoint = "http://localhost:8081/api/chat/completions"
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        for m in body.get("messages", []):
            if m.get("role") == "user" and isinstance(m.get("content"), list):
                texts = [i.get("text", "") for i in m["content"] if i.get("type") == "text"]
                for i in m["content"]:
                    if i.get("type") == "image_url":
                        desc = self._describe(i["image_url"].get("url", ""))
                        m["content"] = " ".join(texts) + f"\n\n[圖片描述: {desc}]"
                        break
        return body
    def _describe(self, url: str) -> str:
        try:
            r = requests.post(self.vision_endpoint, json={"model": self.vision_model, "messages": [{"role": "user", "content": [{"type": "text", "text": "請描述這張圖片"}, {"type": "image_url", "image_url": {"url": url}}]}], "stream": False})
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[無法描述圖片: {e}]"
