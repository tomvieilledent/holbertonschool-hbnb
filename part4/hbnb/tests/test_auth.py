from tests.helpers import auth_headers, login


def test_login_success_returns_access_token(client, admin_user):
    response = login(client, admin_user["email"], admin_user["password"])

    assert response.status_code == 200
    payload = response.get_json()
    assert "access_token" in payload
    assert isinstance(payload["access_token"], str)


def test_login_bad_credentials_returns_401(client, admin_user):
    response = login(client, admin_user["email"], "wrong-password")

    assert response.status_code == 401


def test_protected_requires_jwt_returns_401(client):
    response = client.get("/api/v1/auth/protected")

    assert response.status_code == 401


def test_protected_with_token_returns_200(client, admin_user):
    token = login(client, admin_user["email"], admin_user["password"]).get_json()[
        "access_token"]
    response = client.get("/api/v1/auth/protected",
                          headers=auth_headers(token))

    assert response.status_code == 200
    assert "message" in response.get_json()
