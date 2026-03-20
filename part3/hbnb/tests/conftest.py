import os
import tempfile

import pytest

from app import create_app, db
from app.services import facade

from tests.helpers import auth_headers, login, unique_email


@pytest.fixture()
def app():
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    class TestConfig:
        TESTING = True
        DEBUG = False
        SECRET_KEY = "test-secret-key"
        JWT_SECRET_KEY = "test-jwt-secret-key-32-bytes-minimum"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    app_instance = create_app(TestConfig)

    ctx = app_instance.app_context()
    ctx.push()
    db.session.remove()
    db.drop_all()
    db.create_all()

    yield app_instance

    db.session.remove()
    db.drop_all()
    ctx.pop()
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin_user(app):
    password = "adminpass"
    user = facade.create_user(
        {
            "first_name": "Admin",
            "last_name": "User",
            "email": unique_email("admin"),
            "password": password,
            "is_admin": True,
        }
    )
    return {"id": user.id, "email": user.email, "password": password}


@pytest.fixture()
def normal_user(app):
    password = "userpass"
    user = facade.create_user(
        {
            "first_name": "Normal",
            "last_name": "User",
            "email": unique_email("user"),
            "password": password,
            "is_admin": False,
        }
    )
    return {"id": user.id, "email": user.email, "password": password}


@pytest.fixture()
def admin_token(client, admin_user):
    response = login(client, admin_user["email"], admin_user["password"])
    assert response.status_code == 200
    return response.get_json()["access_token"]


@pytest.fixture()
def normal_token(client, normal_user):
    response = login(client, normal_user["email"], normal_user["password"])
    assert response.status_code == 200
    return response.get_json()["access_token"]


@pytest.fixture()
def admin_headers(admin_token):
    return auth_headers(admin_token)


@pytest.fixture()
def user_headers(normal_token):
    return auth_headers(normal_token)
