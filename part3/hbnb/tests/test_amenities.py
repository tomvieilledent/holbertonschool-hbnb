from tests.helpers import unique_email


def test_amenities_get_list_public_returns_200(client):
    response = client.get("/api/v1/amenities/")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_amenities_post_requires_auth_returns_401(client):
    response = client.post("/api/v1/amenities/", json={"name": "WiFi"})

    assert response.status_code == 401


def test_amenities_post_non_admin_returns_403(client, user_headers):
    response = client.post(
        "/api/v1/amenities/",
        json={"name": "WiFi"},
        headers=user_headers,
    )

    assert response.status_code == 403


def test_amenities_post_admin_creates(client, admin_headers):
    response = client.post(
        "/api/v1/amenities/",
        json={"name": "WiFi"},
        headers=admin_headers,
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "WiFi"


def test_amenities_post_invalid_payload_returns_400(client, admin_headers):
    response = client.post(
        "/api/v1/amenities/",
        json={"name": ""},
        headers=admin_headers,
    )

    assert response.status_code == 400


def test_amenities_get_one_unknown_returns_404(client):
    response = client.get("/api/v1/amenities/not-found")

    assert response.status_code == 404


def test_amenities_put_admin_updates(client, admin_headers):
    create_response = client.post(
        "/api/v1/amenities/",
        json={"name": "Pool"},
        headers=admin_headers,
    )
    amenity_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/v1/amenities/{amenity_id}",
        json={"name": "Pool XXL"},
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "Pool XXL"


def test_amenities_put_non_admin_returns_403(client, admin_headers, user_headers):
    create_response = client.post(
        "/api/v1/amenities/",
        json={"name": "Sauna"},
        headers=admin_headers,
    )
    amenity_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/v1/amenities/{amenity_id}",
        json={"name": "Sauna 2"},
        headers=user_headers,
    )

    assert response.status_code == 403


def test_amenities_delete_admin_returns_200(client, admin_headers):
    create_response = client.post(
        "/api/v1/amenities/",
        json={"name": "Gym"},
        headers=admin_headers,
    )
    amenity_id = create_response.get_json()["id"]

    response = client.delete(
        f"/api/v1/amenities/{amenity_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200


def test_amenities_delete_not_found_returns_404(client, admin_headers):
    response = client.delete(
        "/api/v1/amenities/not-found", headers=admin_headers)

    assert response.status_code == 404
