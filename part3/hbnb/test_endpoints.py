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
        """Build JWT authorization headers."""
        return {'Authorization': f'Bearer {token}'}

    def create_place(self, token, title='Cozy Apartment', **overrides):
        """Create a place through the protected API."""
        payload = {
            'title': title,
            'description': 'A nice place to stay',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'amenities': [],
        }
        payload.update(overrides)
        response = self.client.post(
            '/api/v1/places/',
            json=payload,
            headers=self.auth_headers(token),
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def create_review(self, token, place_id, text='Great place!', rating=5):
        """Create a review through the protected API."""
        return self.client.post(
            '/api/v1/reviews/',
            json={'text': text, 'rating': rating, 'place_id': place_id},
            headers=self.auth_headers(token),
        )


class TestAmenityEndpoints(BaseEndpointTestCase):
    """Amenity endpoints remain public CRUD endpoints."""

    def test_create_amenity_valid(self):
        """Creating an amenity with valid data succeeds."""
        response = self.client.post('/api/v1/amenities/', json={
            'name': f'WiFi-{uuid.uuid4()}',
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_get_all_amenities(self):
        """Listing amenities remains public."""
        fake_amenity = SimpleNamespace(id='amenity-1', name='WiFi')
        with patch('app.api.v1.amenities.facade.get_all_amenities', return_value=[fake_amenity]):
            response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)


class TestUserEndpoints(BaseEndpointTestCase):
    """User endpoints with public creation and protected updates."""

    def test_create_user_valid(self):
        """User creation still works publicly."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': f'john.{uuid.uuid4()}@example.com',
            'password': 'secret123',
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_update_own_user_requires_jwt(self):
        """Updating a user without a token is rejected."""
        user = self.create_user()
        response = self.client.put(
            f"/api/v1/users/{user['id']}",
            json={'first_name': 'Updated'},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_own_user_allows_name_change(self):
        """A user can update their own non-sensitive fields."""
        user = self.create_user()
        token = self.login(user['email'], user['password'])
        response = self.client.put(
            f"/api/v1/users/{user['id']}",
            json={'first_name': 'Updated'},
            headers=self.auth_headers(token),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['first_name'], 'Updated')

    def test_update_user_rejects_other_user(self):
        """A user cannot update another user's details."""
        owner = self.create_user(email=f'owner.{uuid.uuid4()}@example.com')
        intruder = self.create_user(
            email=f'intruder.{uuid.uuid4()}@example.com')
        intruder_token = self.login(intruder['email'], intruder['password'])
        response = self.client.put(
            f"/api/v1/users/{owner['id']}",
            json={'first_name': 'Hacked'},
            headers=self.auth_headers(intruder_token),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'message'], 'Unauthorized action.')

    def test_update_user_rejects_email_or_password(self):
        """A user cannot modify email or password on this endpoint."""
        user = self.create_user()
        token = self.login(user['email'], user['password'])
        response = self.client.put(
            f"/api/v1/users/{user['id']}",
            json={'email': f'new.{uuid.uuid4()}@example.com'},
            headers=self.auth_headers(token),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'],
            'You cannot modify email or password.'
        )


class TestPlaceEndpoints(BaseEndpointTestCase):
    """Place endpoints with public reads and owner-only writes."""

    def test_get_all_places_is_public(self):
        """Listing places stays public and returns price in summaries."""
        fake_place = SimpleNamespace(
            id='place-1', title='Public Place', price=120.0)
        with patch('app.api.v1.places.facade.get_all_places', return_value=[fake_place]):
            response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertIn('price', response.get_json()[0])

    def test_get_place_by_id_is_public(self):
        """Reading one place stays public."""
        fake_owner = SimpleNamespace(
            id='owner-1', first_name='Jane', last_name='Doe', email='jane@example.com')
        fake_place = SimpleNamespace(
            id='place-1',
            title='Public Place',
            description='Nice stay',
            price=120.0,
            latitude=1.0,
            longitude=2.0,
            owner=fake_owner,
            amenities=[],
            reviews=[],
        )
        with patch('app.api.v1.places.facade.get_place', return_value=fake_place):
            response = self.client.get('/api/v1/places/place-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'Public Place')

    def test_create_place_requires_jwt(self):
        """Place creation requires a JWT."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'No Token',
            'price': 50.0,
            'latitude': 1.0,
            'longitude': 2.0,
            'amenities': [],
        })
        self.assertEqual(response.status_code, 401)

    def test_create_place_uses_authenticated_user_as_owner(self):
        """The owner is taken from the token, not from the payload."""
        owner = self.create_user(email=f'owner.{uuid.uuid4()}@example.com')
        other = self.create_user(email=f'other.{uuid.uuid4()}@example.com')
        token = self.login(owner['email'], owner['password'])

        response = self.client.post(
            '/api/v1/places/',
            json={
                'title': 'Owner Bound',
                'description': 'Owned by token user',
                'price': 75.0,
                'latitude': 1.0,
                'longitude': 2.0,
                'owner_id': other['id'],
                'amenities': [],
            },
            headers=self.auth_headers(token),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['owner_id'], owner['id'])

    def test_update_place_rejects_non_owner(self):
        """Only the place owner can update it."""
        owner = self.create_user(email=f'owner.{uuid.uuid4()}@example.com')
        guest = self.create_user(email=f'guest.{uuid.uuid4()}@example.com')
        guest_token = self.login(guest['email'], guest['password'])
        fake_place = SimpleNamespace(owner=SimpleNamespace(id=owner['id']))

        with patch('app.api.v1.places.facade.get_place', return_value=fake_place):
            response = self.client.put(
                '/api/v1/places/place-1',
                json={'title': 'Hacked'},
                headers=self.auth_headers(guest_token),
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'message'], 'Unauthorized action.')

    def test_update_place_allows_owner(self):
        """The owner can update the place."""
        owner = self.create_user()
        token = self.login(owner['email'], owner['password'])
        fake_owner = SimpleNamespace(id=owner['id'])
        fake_place = SimpleNamespace(
            id='place-1',
            title='Updated Title',
            description='A nice place to stay',
            price=100.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner=fake_owner,
            amenities=[],
        )

        with patch('app.api.v1.places.facade.get_place', return_value=fake_place), patch(
            'app.api.v1.places.facade.update_place', return_value=fake_place
        ):
            response = self.client.put(
                '/api/v1/places/place-1',
                json={'title': 'Updated Title'},
                headers=self.auth_headers(token),
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'Updated Title')


class TestReviewEndpoints(BaseEndpointTestCase):
    """Review endpoints with JWT and ownership rules."""

    def test_create_review_requires_jwt(self):
        """Review creation requires a JWT."""
        owner = self.create_user()
        owner_token = self.login(owner['email'], owner['password'])
        place = self.create_place(owner_token)

        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Great place!',
            'rating': 5,
            'place_id': place['id'],
        })
        self.assertEqual(response.status_code, 401)

    def test_create_review_rejects_own_place(self):
        """A place owner cannot review their own place."""
        owner = self.create_user()
        owner_token = self.login(owner['email'], owner['password'])
        fake_place = SimpleNamespace(owner=SimpleNamespace(id=owner['id']))

        with patch('app.api.v1.reviews.facade.get_place', return_value=fake_place):
            response = self.create_review(owner_token, 'place-1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'],
            'You cannot review your own place.'
        )

    def test_create_review_rejects_duplicate_review(self):
        """A user can only review a place once."""
        owner = self.create_user(email=f'owner.{uuid.uuid4()}@example.com')
        guest = self.create_user(email=f'guest.{uuid.uuid4()}@example.com')
        guest_token = self.login(guest['email'], guest['password'])
        fake_place = SimpleNamespace(owner=SimpleNamespace(id=owner['id']))
        existing_review = SimpleNamespace(user=SimpleNamespace(id=guest['id']))

        with patch('app.api.v1.reviews.facade.get_place', return_value=fake_place), patch(
            'app.api.v1.reviews.facade.get_reviews_by_place', return_value=[existing_review]
        ):
            second_response = self.create_review(
                guest_token, 'place-1', text='Again')
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(
            second_response.get_json()['message'],
            'You have already reviewed this place'
        )

    def test_update_review_rejects_non_author(self):
        """Only the review author can update it."""
        owner = self.create_user(email=f'owner.{uuid.uuid4()}@example.com')
        author = self.create_user(email=f'author.{uuid.uuid4()}@example.com')
        intruder = self.create_user(
            email=f'intruder.{uuid.uuid4()}@example.com')
        intruder_token = self.login(intruder['email'], intruder['password'])
        fake_review = SimpleNamespace(user=SimpleNamespace(id=author['id']))

        with patch('app.api.v1.reviews.facade.get_review', return_value=fake_review):
            response = self.client.put(
                '/api/v1/reviews/review-1',
                json={'text': 'Edited', 'rating': 4},
                headers=self.auth_headers(intruder_token),
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'message'], 'Unauthorized action.')

    def test_delete_review_rejects_non_author(self):
        """Only the review author can delete it."""
        owner = self.create_user(email=f'owner.{uuid.uuid4()}@example.com')
        author = self.create_user(email=f'author.{uuid.uuid4()}@example.com')
        intruder = self.create_user(
            email=f'intruder.{uuid.uuid4()}@example.com')
        intruder_token = self.login(intruder['email'], intruder['password'])
        fake_review = SimpleNamespace(user=SimpleNamespace(id=author['id']))

        with patch('app.api.v1.reviews.facade.get_review', return_value=fake_review):
            response = self.client.delete(
                '/api/v1/reviews/review-1',
                headers=self.auth_headers(intruder_token),
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()[
                         'message'], 'Unauthorized action.')

    def test_delete_missing_review_returns_404(self):
        """Deleting a missing review returns 404 instead of 500."""
        user = self.create_user()
        token = self.login(user['email'], user['password'])
        with patch('app.api.v1.reviews.facade.get_review', return_value=None):
            response = self.client.delete(
                '/api/v1/reviews/missing-review-id',
                headers=self.auth_headers(token),
            )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['message'], 'Review not found')


if __name__ == '__main__':
    unittest.main()
