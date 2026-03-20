from tests.helpers import login


def create_place(client, headers):
    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Review place",
            "description": "A place to review",
            "price": 89.9,
            "latitude": 40.0,
            "longitude": 2.0,
            "amenities": [],
        },
        headers=headers,
    )
    assert response.status_code == 201
    return response.get_json()


def test_reviews_get_list_public_returns_200(client):
    response = client.get("/api/v1/reviews/")

    assert response.status_code == 200


def test_reviews_post_requires_auth_returns_401(client):
    response = client.post(
        "/api/v1/reviews/",
        json={"text": "Great", "rating": 5, "place_id": "x"},
    )

    assert response.status_code == 401


def test_reviews_post_invalid_payload_returns_400(client, user_headers):
    response = client.post(
        "/api/v1/reviews/",
        json={"text": "Missing fields"},
        headers=user_headers,
    )

    assert response.status_code == 400


def test_reviews_post_place_not_found_returns_404(client, user_headers):
    response = client.post(
        "/api/v1/reviews/",
        json={"text": "Great", "rating": 5, "place_id": "not-found"},
        headers=user_headers,
    )

    assert response.status_code == 404


def test_reviews_owner_cannot_review_own_place_returns_400(client, user_headers):
    place = create_place(client, user_headers)

    response = client.post(
        "/api/v1/reviews/",
        json={"text": "I review myself", "rating": 4, "place_id": place["id"]},
        headers=user_headers,
    )

    assert response.status_code == 400


def test_reviews_user_can_create_review(client, admin_headers, normal_user, normal_token):
    owner_create = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Owner",
            "last_name": "Place",
            "email": "owner.place@example.com",
            "password": "ownerpass",
        },
        headers=admin_headers,
    )
    assert owner_create.status_code == 201

    owner_login = login(client, "owner.place@example.com", "ownerpass")
    owner_token = owner_login.get_json()["access_token"]
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    place = create_place(client, owner_headers)

    response = client.post(
        "/api/v1/reviews/",
        json={"text": "Great stay", "rating": 5, "place_id": place["id"]},
        headers={"Authorization": f"Bearer {normal_token}"},
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["place_id"] == place["id"]


def test_reviews_put_non_owner_returns_403(client, admin_headers, normal_token):
    owner_create = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Review",
            "last_name": "Owner",
            "email": "review.owner@example.com",
            "password": "ownerpass",
        },
        headers=admin_headers,
    )
    assert owner_create.status_code == 201

    owner_login = login(client, "review.owner@example.com", "ownerpass")
    owner_token = owner_login.get_json()["access_token"]
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    place = create_place(client, owner_headers)

    review_create = client.post(
        "/api/v1/reviews/",
        json={"text": "Initial", "rating": 4, "place_id": place["id"]},
        headers={"Authorization": f"Bearer {normal_token}"},
    )
    review_id = review_create.get_json()["id"]

    intruder = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Intruder",
            "last_name": "User",
            "email": "intruder.user@example.com",
            "password": "intruderpass",
        },
        headers=admin_headers,
    )
    assert intruder.status_code == 201
    intruder_login = login(client, "intruder.user@example.com", "intruderpass")
    intruder_token = intruder_login.get_json()["access_token"]

    response = client.put(
        f"/api/v1/reviews/{review_id}",
        json={"text": "Hack", "rating": 1},
        headers={"Authorization": f"Bearer {intruder_token}"},
    )

    assert response.status_code == 403


def test_reviews_delete_owner_returns_200(client, admin_headers, normal_token):
    owner_create = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Delete",
            "last_name": "Owner",
            "email": "delete.owner@example.com",
            "password": "ownerpass",
        },
        headers=admin_headers,
    )
    assert owner_create.status_code == 201

    owner_login = login(client, "delete.owner@example.com", "ownerpass")
    owner_token = owner_login.get_json()["access_token"]
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    place = create_place(client, owner_headers)

    review_create = client.post(
        "/api/v1/reviews/",
        json={"text": "To delete", "rating": 5, "place_id": place["id"]},
        headers={"Authorization": f"Bearer {normal_token}"},
    )
    review_id = review_create.get_json()["id"]

    response = client.delete(
        f"/api/v1/reviews/{review_id}",
        headers={"Authorization": f"Bearer {normal_token}"},
    )

    assert response.status_code == 200


def test_reviews_get_unknown_returns_404(client):
    response = client.get("/api/v1/reviews/not-found")

    assert response.status_code == 404
