from pathlib import Path
from see.core import Harness,ProviderRegistry
def test_bootstrap(tmp_path):
 h=Harness(tmp_path); assert h.bootstrap(); assert len(h.tree.nodes())>=10
def test_providers(): assert "openai" in ProviderRegistry.providers and "litellm" in ProviderRegistry.providers


def test_openai_compatible_provider():
    registry = ProviderRegistry()
    ready = registry.ready({"OPENAI_COMPATIBLE_BASE_URL": "https://example.invalid/v1"})
    assert ready["openai_compatible"]
    assert ready["openai"]
