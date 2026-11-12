"""HTTP client for the installed OpenHands 0.47.0 web API."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx


class OpenHandsAPIError(RuntimeError):
    """Raised when the OpenHands API returns an error."""


class OpenHandsClient:
    def __init__(self, base_url: str = "http://127.0.0.1:13000", timeout: float = 20.0):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url, timeout=timeout)

    def close(self) -> None:
        self.client.close()

    def health(self) -> dict[str, Any]:
        response = self.client.get("/health")
        if response.is_error:
            raise OpenHandsAPIError(f"OpenHands health check failed: HTTP {response.status_code}")
        data = response.json()
        return data if isinstance(data, dict) else {"status": data}

    def create_conversation(self, initial_user_msg: str, repository: str | None = None,
                            selected_branch: str | None = None,
                            conversation_instructions: str | None = None) -> dict[str, Any]:
        if not initial_user_msg.strip():
            raise ValueError("initial_user_msg must not be empty")
        payload: dict[str, Any] = {"initial_user_msg": initial_user_msg}
        if repository:
            payload["repository"] = repository
        if selected_branch:
            payload["selected_branch"] = selected_branch
        if conversation_instructions:
            payload["conversation_instructions"] = conversation_instructions
        response = self.client.post("/api/conversations", json=payload)
        if response.is_error:
            raise OpenHandsAPIError(f"OpenHands conversation creation failed: HTTP {response.status_code} {response.text[:500]}")
        data = response.json()
        if not data.get("conversation_id"):
            raise OpenHandsAPIError("OpenHands response did not contain conversation_id")
        return data

    def start_conversation(self, conversation_id: str) -> dict[str, Any]:
        if not conversation_id.strip():
            raise ValueError("conversation_id must not be empty")
        path = f"/api/conversations/{quote(conversation_id, safe='')}/start"
        response = self.client.post(path, json={})
        if response.is_error:
            raise OpenHandsAPIError(f"OpenHands start failed: HTTP {response.status_code} {response.text[:500]}")
        data = response.json()
        return data if isinstance(data, dict) else {"result": data}

    def list_conversations(self) -> dict[str, Any]:
        response = self.client.get("/api/conversations")
        if response.is_error:
            raise OpenHandsAPIError(f"OpenHands list failed: HTTP {response.status_code}")
        data = response.json()
        return data if isinstance(data, dict) else {"results": data}
