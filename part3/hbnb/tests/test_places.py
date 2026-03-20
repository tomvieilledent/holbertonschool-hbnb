from tests.helpers import unique_email


def create_place_payload():
    return {
        "title": "Nice flat",
        "description": "Center city",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "amenities": [],
    }


def test_places_get_list_public_returns_200(client):
    response = client.get("/api/v1/places/")

    assert response.status_code == 200


def test_places_post_requires_auth_returns_401(client):
    response = client.post("/api/v1/places/", json=create_place_payload())

    assert response.status_code == 401


def test_places_post_user_creates_place(client, user_headers):
    response = client.post(
        "/api/v1/places/",
        json=create_place_payload(),
        headers=user_headers,
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["title"] == "Nice flat"
    assert payload["owner_id"] is not None


def test_places_post_invalid_payload_returns_400(client, user_headers):
    payload = create_place_payload()
    payload["price"] = -1

    response = client.post(
        "/api/v1/places/", json=payload, headers=user_headers)

    assert response.status_code == 400


def test_places_get_one_unknown_returns_404(client):
    response = client.get("/api/v1/places/not-found")

    assert response.status_code == 404


def test_places_put_non_owner_returns_403(client, user_headers, admin_headers):
    create_response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Other",
            "last_name": "Owner",
            "email": unique_email("other"),
            "password": "otherpass",
        },
        headers=admin_headers,
    )
    other_user = create_response.get_json()

    from tests.helpers import login

    other_token = login(client, other_user["email"], "otherpass").get_json()[
        "access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    place_response = client.post(
        "/api/v1/places/",
        json=create_place_payload(),
        headers=other_headers,
    )
    place_id = place_response.get_json()["id"]

    response = client.put(
        f"/api/v1/places/{place_id}",
        json={"title": "Hacked"},
        headers=user_headers,
    )

    assert response.status_code == 403


def test_places_put_owner_updates(client, user_headers):
    place_response = client.post(
        "/api/v1/places/",
        json=create_place_payload(),
        headers=user_headers,
    )
    place_id = place_response.get_json()["id"]

    response = client.put(
        f"/api/v1/places/{place_id}",
        json={"title": "Updated title"},
        headers=user_headers,
    )

    assert response.status_code == 200
    assert response.get_json()["title"] == "Updated title"


def test_places_delete_non_owner_returns_403(client, user_headers, admin_headers):
    create_response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Delete",
            "last_name": "Owner",
            "email": unique_email("delowner"),
            "password": "otherpass",
        },
        headers=admin_headers,
    )
    other_user = create_response.get_json()

    from tests.helpers import login

    other_token = login(client, other_user["email"], "otherpass").get_json()[
        "access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    place_response = client.post(
        "/api/v1/places/",
        json=create_place_payload(),
        headers=other_headers,
    )
    place_id = place_response.get_json()["id"]

    response = client.delete(
        f"/api/v1/places/{place_id}", headers=user_headers)

    assert response.status_code == 403


def test_places_delete_owner_returns_200(client, user_headers):
    place_response = client.post(
        "/api/v1/places/",
        json=create_place_payload(),
        headers=user_headers,
    )
    place_id = place_response.get_json()["id"]

    response = client.delete(
        f"/api/v1/places/{place_id}", headers=user_headers)

    assert response.status_code == 200


def test_places_reviews_unknown_place_returns_404(client):
    response = client.get("/api/v1/places/not-found/reviews")

    assert response.status_code == 404
