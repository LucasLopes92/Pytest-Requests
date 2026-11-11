from __future__ import annotations

import os

import pytest

from api.client import ApiClient


@pytest.fixture
def api_client() -> ApiClient:
    client = ApiClient(
        base_url=os.getenv("DUMMYJSON_BASE_URL", "https://dummyjson.com"),
        timeout=float(os.getenv("REQUEST_TIMEOUT", "10")),
    )
    yield client
    client.close()


@pytest.fixture
def demo_credentials() -> dict[str, str]:
    """Credenciais fictícias de demonstração; podem ser sobrescritas no ambiente."""
    return {
        "username": os.getenv("DUMMYJSON_USERNAME", "emilys"),
        "password": os.getenv("DUMMYJSON_PASSWORD", "emilyspass"),
    }
