import src.sdk.client as client_module
from src.sdk.client import OrchestratorClient


class DummyResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return b'{"ok": true}'


def test_request_normalizes_base_url_before_joining_api_path(monkeypatch):
    seen = {}

    def fake_urlopen(request):
        seen["url"] = request.full_url
        return DummyResponse()

    monkeypatch.setattr(client_module, "urlopen", fake_urlopen)

    client = OrchestratorClient(base_url="https://example.test/", api_key="test-key")

    assert client.list_agents() == {"ok": True}
    assert client.base_url == "https://example.test"
    assert seen["url"] == "https://example.test/api/v2/agents"
