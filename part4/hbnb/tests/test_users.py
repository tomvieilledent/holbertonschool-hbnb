from app.services import facade
from tests.helpers import login, unique_email


def test_users_get_list_is_public(client, admin_user):
    response = client.get("/api/v1/users/")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_users_post_requires_auth_returns_401(client):
    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email("john"),
            "password": "secret123",
        },
    )

    assert response.status_code == 401


def test_users_post_non_admin_returns_403(client, normal_user, normal_token):
    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email("jane"),
            "password": "secret123",
        },
        headers={"Authorization": f"Bearer {normal_token}"},
    )

    assert response.status_code == 403


def test_users_post_admin_creates_user(client, admin_headers):
    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Alice",
            "last_name": "Martin",
            "email": unique_email("alice"),
            "password": "secret123",
        },
        headers=admin_headers,
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["email"].startswith("alice.")


def test_users_post_invalid_payload_returns_400(client, admin_headers):
    response = client.post(
        "/api/v1/users/",
        json={"first_name": "OnlyOneField"},
        headers=admin_headers,
    )

    assert response.status_code == 400


def test_users_get_one_returns_404_for_unknown(client):
    response = client.get("/api/v1/users/not-found")

    assert response.status_code == 404


def test_users_put_non_owner_non_admin_returns_403(client, app, admin_headers, normal_user):
    target_user = facade.create_user(
        {
            "first_name": "Target",
            "last_name": "User",
            "email": unique_email("target"),
            "password": "target123",
            "is_admin": False,
        }
    )

    normal_token = login(
        client, normal_user["email"], normal_user["password"]).get_json()["access_token"]
    response = client.put(
        f"/api/v1/users/{target_user.id}",
        json={"first_name": "Hacker"},
        headers={"Authorization": f"Bearer {normal_token}"},
    )

    assert response.status_code == 403


def test_users_put_owner_cannot_change_email_returns_400(client, normal_user):
    normal_token = login(
        client, normal_user["email"], normal_user["password"]).get_json()["access_token"]

    response = client.put(
        f"/api/v1/users/{normal_user['id']}",
        json={"email": unique_email("new")},
        headers={"Authorization": f"Bearer {normal_token}"},
    )

    assert response.status_code == 400


def test_users_put_admin_can_update_user(client, admin_headers):
    create_response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Bob",
            "last_name": "M",
            "email": unique_email("bob"),
            "password": "oldpass",
        },
        headers=admin_headers,
    )
    user_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/v1/users/{user_id}",
        json={"password": "newpass123"},
        headers=admin_headers,
    )

    assert response.status_code == 200
