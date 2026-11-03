"""
Lody 应用连接器 - 同步任务和结果
"""
 
import os
import requests
import json
from typing import Dict, Any
 
class LodyConnector:
    """Connect to Lody app for task distribution and result sync"""
 
    def __init__(self):
        self.server = os.getenv("LODY_SERVER", "http://localhost:8008")
        self.user_id = os.getenv("LODY_USER_ID", "default")
        self.room_id = os.getenv("LODY_ROOM_ID", "ai-agents")
        self.enabled = os.getenv("LODY_ENABLED", "true").lower() == "true"
 
        self.api_url = f"{self.server}/api/v1"
 
    def is_enabled(self) -> bool:
        return self.enabled
 
    def fetch_tasks(self) -> list:
        """从 Lody 获取待处理任务"""
        if not self.enabled:
            return []
 
        try:
            url = f"{self.api_url}/tasks/pending"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ Fetched tasks from Lody")
                return response.json()
        except Exception as e:
            print(f"⚠️  Lody fetch error: {e}")
 
        return []
 
    def send_result(self, task_id: str, result: Dict[str, Any]) -> bool:
        """发送结果到 Lody"""
        if not self.enabled:
            return False
 
        try:
            url = f"{self.api_url}/tasks/{task_id}/result"
            payload = {
                "status": "completed",
                "result": result,
                "user_id": self.user_id,
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code in [200, 201]:
                print(f"✅ Result sent to Lody for task {task_id}")
                return True
        except Exception as e:
            print(f"⚠️  Lody send error: {e}")
 
        return False
 
    def broadcast_to_room(self, message: str) -> bool:
        """广播消息到 Lody 房间"""
        if not self.enabled:
            return False
 
        try:
            url = f"{self.api_url}/rooms/{self.room_id}/message"
            payload = {
                "text": message,
                "sender": "ai-agent",
                "type": "status",
            }
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"⚠️  Lody broadcast error: {e}")
 
        return False
 
# Global instance
_lody_connector = None
 
def get_lody_connector() -> LodyConnector:
    global _lody_connector
    if _lody_connector is None:
        _lody_connector = LodyConnector()
    return _lody_connector
