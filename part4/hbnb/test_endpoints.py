#!/usr/bin/python3
"""Integration tests for JWT auth, admin access, and DB-backed endpoints."""

import os
import tempfile
import unittest
import uuid

from app import create_app, db
from app.services import facade


class DatabaseTestCase(unittest.TestCase):
    """Isolated SQLite-backed test case."""

    def setUp(self):
        fd, db_path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        self.db_path = db_path

        class TestConfig:
            TESTING = True
            DEBUG = False
            SECRET_KEY = 'test-secret-key-32-bytes-minimum-value'
            JWT_SECRET_KEY = 'test-jwt-secret-key-32-bytes-minimum-value'
            SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
            SQLALCHEMY_TRACK_MODIFICATIONS = False

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def unique_email(self, prefix='user'):
        return f'{prefix}.{uuid.uuid4()}@example.com'

    def create_admin_direct(self, password='secret123'):
        email = self.unique_email('admin')
        user = facade.create_user({
            'first_name': 'Admin',
            'last_name': 'User',
            'email': email,
            'password': password,
            'is_admin': True,
        })
        return {'id': user.id, 'email': email, 'password': password}

    def login(self, email, password):
        response = self.client.post('/api/v1/auth/login', json={
            'email': email,
            'password': password,
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()['access_token']

    def auth_headers(self, token):
        return {'Authorization': f'Bearer {token}'}

    def create_user_as_admin(self, admin_token, first_name='Regular', last_name='User',
                             email=None, password='secret123', is_admin=False):
        user_email = email or self.unique_email('user')
        response = self.client.post('/api/v1/users/', json={
            'first_name': first_name,
            'last_name': last_name,
            'email': user_email,
            'password': password,
            'is_admin': is_admin,
        }, headers=self.auth_headers(admin_token))
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        payload['email'] = user_email
        payload['password'] = password
        return payload

    def create_place(self, token):
        response = self.client.post('/api/v1/places/', json={
            'title': 'Cozy apartment',
            'description': 'Comfortable city stay',
            'price': 120.5,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'amenities': [],
        }, headers=self.auth_headers(token))
        self.assertEqual(response.status_code, 201)
        return response.get_json()


class AuthEndpointTests(DatabaseTestCase):
    def test_login_returns_token(self):
        admin = self.create_admin_direct()
        response = self.client.post('/api/v1/auth/login', json={
            'email': admin['email'],
            'password': admin['password'],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_protected_requires_token(self):
        response = self.client.get('/api/v1/auth/protected')
        self.assertEqual(response.status_code, 401)


class UserEndpointTests(DatabaseTestCase):
    def test_create_user_requires_jwt(self):
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': self.unique_email(),
            'password': 'secret123',
        })
        self.assertEqual(response.status_code, 401)

    def test_create_user_requires_admin(self):
        admin = self.create_admin_direct()
        admin_token = self.login(admin['email'], admin['password'])
        user = self.create_user_as_admin(admin_token)
        user_token = self.login(user['email'], user['password'])

        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Other',
            'last_name': 'User',
            'email': self.unique_email('other'),
            'password': 'secret123',
        }, headers=self.auth_headers(user_token))
        self.assertEqual(response.status_code, 403)

    def test_non_admin_cannot_update_other_user(self):
        admin = self.create_admin_direct()
        admin_token = self.login(admin['email'], admin['password'])
        owner = self.create_user_as_admin(
            admin_token, email=self.unique_email('owner'))
        guest = self.create_user_as_admin(
            admin_token, email=self.unique_email('guest'))
        guest_token = self.login(guest['email'], guest['password'])

        response = self.client.put(
            f"/api/v1/users/{owner['id']}",
            json={'first_name': 'Intrusion'},
            headers=self.auth_headers(guest_token),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'message'], 'Unauthorized action.')

    def test_non_admin_cannot_change_email_or_password(self):
        admin = self.create_admin_direct()
        admin_token = self.login(admin['email'], admin['password'])
        user = self.create_user_as_admin(admin_token)
        user_token = self.login(user['email'], user['password'])

        response = self.client.put(
            f"/api/v1/users/{user['id']}",
            json={'email': self.unique_email('new')},
            headers=self.auth_headers(user_token),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()[
                         'message'], 'You cannot modify email or password.')

    def test_admin_can_update_user_password(self):
        admin = self.create_admin_direct(password='adminpass')
        admin_token = self.login(admin['email'], admin['password'])
        member = self.create_user_as_admin(admin_token, password='oldpass')

        response = self.client.put(
            f"/api/v1/users/{member['id']}",
            json={'password': 'newpass123'},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(response.status_code, 200)

        relogin = self.client.post('/api/v1/auth/login', json={
            'email': member['email'],
            'password': 'newpass123',
        })
        self.assertEqual(relogin.status_code, 200)


class PlaceEndpointTests(DatabaseTestCase):
    def test_place_owner_is_taken_from_jwt(self):
        admin = self.create_admin_direct()
        admin_token = self.login(admin['email'], admin['password'])
        owner = self.create_user_as_admin(
            admin_token, email=self.unique_email('owner'))
        other = self.create_user_as_admin(
            admin_token, email=self.unique_email('other'))
        owner_token = self.login(owner['email'], owner['password'])

        response = self.client.post('/api/v1/places/', json={
            'title': 'Token owned',
            'description': 'Owner from JWT',
            'price': 95,
            'latitude': 12.3,
            'longitude': 45.6,
            'owner_id': other['id'],
            'amenities': [],
        }, headers=self.auth_headers(owner_token))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['owner_id'], owner['id'])

    def test_non_owner_cannot_update_place(self):
        admin = self.create_admin_direct()
        admin_token = self.login(admin['email'], admin['password'])
        owner = self.create_user_as_admin(
            admin_token, email=self.unique_email('owner'))
        guest = self.create_user_as_admin(
            admin_token, email=self.unique_email('guest'))
        owner_token = self.login(owner['email'], owner['password'])
        guest_token = self.login(guest['email'], guest['password'])
        place = self.create_place(owner_token)

        response = self.client.put(
            f"/api/v1/places/{place['id']}",
            json={'title': 'Intrusion'},
            headers=self.auth_headers(guest_token),
        )
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main(verbosity=2)
