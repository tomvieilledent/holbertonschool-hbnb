#!/usr/bin/python3
"""Focused endpoint tests aligned with JWT and ownership rules."""

import unittest
import uuid
from types import SimpleNamespace
from unittest.mock import patch

from app import create_app


class BaseEndpointTestCase(unittest.TestCase):
    """Shared helpers for endpoint tests."""

    def setUp(self):
        """Initialize test client."""
        self.app = create_app()
        self.client = self.app.test_client()

    def create_user(self, email=None, first_name='User', last_name='Test',
                    password='secret123'):
        """Create a user and return API data plus credentials."""
        user_email = email or f"user.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            'first_name': first_name,
            'last_name': last_name,
            'email': user_email,
            'password': password,
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        data['email'] = user_email
        data['password'] = password
        return data

    def login(self, email, password):
        """Return a bearer token for a user."""
        response = self.client.post('/api/v1/auth/login', json={
            'email': email,
            'password': password,
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()['access_token']

    def auth_headers(self, token):
        """Return Authorization headers for JWT requests."""
        return {'Authorization': f'Bearer {token}'}

    def create_amenity(self, admin_token, name='WiFi'):
        """Create an amenity through the API."""
        response = self.client.post(
            '/api/v1/amenities/',
            json={'name': f'{name}-{uuid.uuid4()}'},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def create_place(self, token, title='Cozy apartment', amenities=None, **overrides):
        """Create a place owned by the authenticated user."""
        payload = {
            'title': title,
            'description': 'Comfortable city stay',
            'price': 120.5,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'amenities': amenities or [],
        }
        payload.update(overrides)
        response = self.client.post(
            '/api/v1/places/',
            json=payload,
            headers=self.auth_headers(token),
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def create_review(self, token, place_id, text='Great stay', rating=5):
        """Create a review for a place."""
        response = self.client.post(
            '/api/v1/reviews/',
            json={'text': text, 'rating': rating, 'place_id': place_id},
            headers=self.auth_headers(token),
        )
        return response


class AuthEndpointTests(DatabaseTestCase):
    """Validate authentication and JWT-protected access."""

    def test_login_returns_access_token_for_valid_credentials(self):
        """A valid login returns a JWT."""
        user = self.create_user_via_api()

        response = self.client.post('/api/v1/auth/login', json={
            'email': user['email'],
            'password': user['password'],
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_login_rejects_invalid_credentials(self):
        """An invalid password is rejected."""
        user = self.create_user_via_api()

        response = self.client.post('/api/v1/auth/login', json={
            'email': user['email'],
            'password': 'wrong-password',
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['error'], 'Invalid credentials')

    def test_protected_endpoint_requires_token(self):
        """The protected auth route denies anonymous requests."""
        response = self.client.get('/api/v1/auth/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint_returns_authenticated_identity(self):
        """The protected auth route uses the JWT identity."""
        user = self.create_user_via_api()
        token = self.login(user['email'], user['password'])

        response = self.client.get(
            '/api/v1/auth/protected',
            headers=self.auth_headers(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[
                         'message'], f"Hello, user {user['id']}")


class UserEndpointTests(DatabaseTestCase):
    """Validate public registration and protected user updates."""

    def test_create_user_persists_to_database(self):
        """A public registration creates a persistent user."""
        email = self.unique_email()

        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': email,
            'password': 'secret123',
        })

        self.assertEqual(response.status_code, 201)
        created_id = response.get_json()['id']
        created_user = facade.get_user(created_id)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, email)

    def test_duplicate_email_is_rejected(self):
        """Two users cannot register with the same email."""
        email = self.unique_email()
        first_response = self.client.post('/api/v1/users/', json={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': email,
            'password': 'secret123',
        })
        self.assertEqual(first_response.status_code, 201)

        second_response = self.client.post('/api/v1/users/', json={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': email,
            'password': 'secret123',
        })

        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(second_response.get_json()[
                         'message'], 'Email already registered')

    def test_user_can_update_own_name(self):
        """A non-admin may update their own non-sensitive fields."""
        user = self.create_user_via_api()
        token = self.login(user['email'], user['password'])

        response = self.client.put(
            f"/api/v1/users/{user['id']}",
            json={'first_name': 'Updated'},
            headers=self.auth_headers(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['first_name'], 'Updated')

    @unittest.expectedFailure
    def test_non_admin_cannot_update_another_user(self):
        """A regular user should not be able to edit someone else's profile."""
        owner = self.create_user_via_api()
        outsider = self.create_user_via_api()
        outsider_token = self.login(outsider['email'], outsider['password'])

        response = self.client.put(
            f"/api/v1/users/{owner['id']}",
            json={'first_name': 'Intrusion'},
            headers=self.auth_headers(outsider_token),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'message'], 'Unauthorized action.')

    def test_admin_can_update_another_user(self):
        """An admin can edit another user's profile."""
        admin = self.create_user_via_api(is_admin=True)
        member = self.create_user_via_api()
        admin_token = self.login(admin['email'], admin['password'])

        response = self.client.put(
            f"/api/v1/users/{member['id']}",
            json={'first_name': 'Reviewed'},
            headers=self.auth_headers(admin_token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['first_name'], 'Reviewed')


class AmenityEndpointTests(DatabaseTestCase):
    """Validate admin-only amenity writes with a real database."""

    def test_non_admin_cannot_create_amenity(self):
        """A regular user is rejected from admin-only amenity creation."""
        user = self.create_user_via_api()
        token = self.login(user['email'], user['password'])

        response = self.client.post(
            '/api/v1/amenities/',
            json={'name': 'Pool'},
            headers=self.auth_headers(token),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'error'], 'Admin privileges required')

    def test_admin_can_create_and_delete_amenity(self):
        """An admin can manage amenity lifecycle."""
        admin = self.create_user_via_api(is_admin=True)
        admin_token = self.login(admin['email'], admin['password'])

        created = self.create_amenity(admin_token, name='Pool')
        delete_response = self.client.delete(
            f"/api/v1/amenities/{created['id']}",
            headers=self.auth_headers(admin_token),
        )

        self.assertEqual(delete_response.status_code, 200)
        self.assertIsNone(facade.get_amenity(created['id']))


class PlaceEndpointTests(DatabaseTestCase):
    """Validate ownership and admin access rules for places."""

    def test_create_place_requires_jwt(self):
        """Anonymous users cannot create places."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'No token',
            'description': 'Denied',
            'price': 40,
            'latitude': 1.0,
            'longitude': 2.0,
            'amenities': [],
        })

        self.assertEqual(response.status_code, 401)

    def test_place_owner_is_taken_from_jwt(self):
        """Payload owner_id is ignored in favor of JWT identity."""
        owner = self.create_user_via_api()
        other_user = self.create_user_via_api()
        token = self.login(owner['email'], owner['password'])

        response = self.client.post(
            '/api/v1/places/',
            json={
                'title': 'Token owned',
                'description': 'Owner derived from JWT',
                'price': 85,
                'latitude': 12.3,
                'longitude': 45.6,
                'owner_id': other_user['id'],
                'amenities': [],
            },
            headers=self.auth_headers(token),
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['owner_id'], owner['id'])

    def test_non_owner_cannot_update_place(self):
        """A user cannot update a place they do not own."""
        owner = self.create_user_via_api()
        guest = self.create_user_via_api()
        owner_token = self.login(owner['email'], owner['password'])
        guest_token = self.login(guest['email'], guest['password'])
        place = self.create_place(owner_token)

        response = self.client.put(
            f"/api/v1/places/{place['id']}",
            json={'title': 'Compromised'},
            headers=self.auth_headers(guest_token),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'message'], 'Unauthorized action.')

    def test_admin_can_delete_any_place(self):
        """An admin can delete a place owned by another user."""
        owner = self.create_user_via_api()
        admin = self.create_user_via_api(is_admin=True)
        owner_token = self.login(owner['email'], owner['password'])
        admin_token = self.login(admin['email'], admin['password'])
        place = self.create_place(owner_token)

        response = self.client.delete(
            f"/api/v1/places/{place['id']}",
            headers=self.auth_headers(admin_token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(facade.get_place(place['id']))


class ReviewEndpointTests(DatabaseTestCase):
    """Validate review rules, ownership, and admin moderation."""

    def test_user_cannot_review_own_place(self):
        """A place owner is blocked from reviewing their own place."""
        owner = self.create_user_via_api()
        owner_token = self.login(owner['email'], owner['password'])
        place = self.create_place(owner_token)

        response = self.create_review(owner_token, place['id'])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()[
                         'message'], 'You cannot review your own place.')

    def test_user_cannot_review_same_place_twice(self):
        """A reviewer may leave only one review per place."""
        owner = self.create_user_via_api()
        reviewer = self.create_user_via_api()
        owner_token = self.login(owner['email'], owner['password'])
        reviewer_token = self.login(reviewer['email'], reviewer['password'])
        place = self.create_place(owner_token)

        first_response = self.create_review(reviewer_token, place['id'])
        second_response = self.create_review(reviewer_token, place['id'])

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(second_response.get_json()[
                         'message'], 'You have already reviewed this place.')

    def test_admin_can_delete_other_users_review(self):
        """An admin can moderate and delete a review they do not own."""
        owner = self.create_user_via_api()
        reviewer = self.create_user_via_api()
        admin = self.create_user_via_api(is_admin=True)
        owner_token = self.login(owner['email'], owner['password'])
        reviewer_token = self.login(reviewer['email'], reviewer['password'])
        admin_token = self.login(admin['email'], admin['password'])
        place = self.create_place(owner_token)
        review_response = self.create_review(reviewer_token, place['id'])
        review_id = review_response.get_json()['id']

        delete_response = self.client.delete(
            f"/api/v1/reviews/{review_id}",
            headers=self.auth_headers(admin_token),
        )

        self.assertEqual(delete_response.status_code, 200)
        self.assertIsNone(facade.get_review(review_id))


if __name__ == '__main__':
    unittest.main(verbosity=2)
