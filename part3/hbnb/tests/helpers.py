import uuid


def unique_email(prefix="user"):
    return f"{prefix}.{uuid.uuid4().hex[:8]}@example.com"


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def login(client, email, password):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    return response
