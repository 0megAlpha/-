import httpx

from agent_os.openhands_client import OpenHandsClient


def test_health_uses_local_api():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/health"
        return httpx.Response(200, json={"status": "OK"})

    client = OpenHandsClient()
    client.client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://test")
    assert client.health() == {"status": "OK"}
    client.close()


def test_create_and_start_conversation():
    calls: list[tuple[str, dict]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        import json
        body = json.loads(request.content or b"{}")
        calls.append((request.method + " " + request.url.path, body))
        if request.url.path == "/api/conversations":
            return httpx.Response(200, json={"conversation_id": "test-123", "status": "STOPPED"})
        if request.url.path == "/api/conversations/test-123/start":
            return httpx.Response(200, json={"status": "STARTING"})
        return httpx.Response(404)

    client = OpenHandsClient()
    client.client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://test")
    created = client.create_conversation("Implement the approved task", repository="https://github.com/0megAlpha/demo")
    started = client.start_conversation(created["conversation_id"])
    assert started["status"] == "STARTING"
    assert calls[0][1]["initial_user_msg"] == "Implement the approved task"
    assert calls[1][0].endswith("/start")
    client.close()
