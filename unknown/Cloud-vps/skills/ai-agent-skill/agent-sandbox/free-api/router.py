#!/usr/bin/env python3
import json, os, requests
from pathlib import Path
class FreeAPIRouter:
    def __init__(self, config_dir="/opt/free-api/config"):
        self.config_dir = Path(config_dir)
        self.providers = {json.loads(f.read_text())["provider"]: json.loads(f.read_text()) for f in self.config_dir.glob("*.json")}
    def route_request(self, provider, endpoint, payload):
        cfg = self.providers[provider]
        headers = {"Content-Type": "application/json"}
        key = os.getenv(cfg.get("api_key_env", ""), "")
        if key: headers["Authorization"] = f"Bearer {key}"
        r = requests.post(f"{cfg['base_url']}/{endpoint}", json=payload, headers=headers)
        r.raise_for_status()
        return r.json()
    def list_providers(self): return list(self.providers)
    def get_free_models(self, provider): return self.providers.get(provider, {}).get("free_models", [])
if __name__ == "__main__":
    print("Available providers:", FreeAPIRouter().list_providers())
