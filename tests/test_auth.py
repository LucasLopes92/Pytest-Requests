"""Cenários de autenticação da DummyJSON."""


def test_login_returns_access_token(api_client, demo_credentials):
    response = api_client.post("/auth/login", json=demo_credentials)

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == demo_credentials["username"]
    assert isinstance(body.get("id"), int)
    assert body.get("accessToken")
    assert body.get("refreshToken")


def test_authenticated_user_endpoint_returns_logged_in_user(
    api_client, demo_credentials
):
    login_response = api_client.post("/auth/login", json=demo_credentials)
    assert login_response.status_code == 200, "Não foi possível autenticar o usuário de teste"

    access_token = login_response.json().get("accessToken")
    assert access_token, "A resposta de login não contém accessToken"

    response = api_client.get("/auth/me", token=access_token)

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == demo_credentials["username"]
    assert isinstance(body.get("id"), int)
    assert "email" in body
