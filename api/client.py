"""Cliente HTTP pequeno e reutilizável para a API DummyJSON."""

from __future__ import annotations

import requests


class ApiClient:
    """Centraliza URL-base, timeout e sessão HTTP para os testes."""

    def __init__(self, base_url: str, timeout: float = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def post(self, path: str, *, json: dict) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/{path.lstrip('/')}",
            json=json,
            timeout=self.timeout,
        )

    def get(
        self,
        path: str,
        *,
        token: str | None = None,
        params: dict[str, str | int] | None = None,
    ) -> requests.Response:
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return self.session.get(
            f"{self.base_url}/{path.lstrip('/')}",
            headers=headers,
            params=params,
            timeout=self.timeout,
        )

    def close(self) -> None:
        self.session.close()
