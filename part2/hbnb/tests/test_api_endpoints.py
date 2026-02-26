#!/usr/bin/python3

import unittest

from app import create_app
from app.services import facade


class TestAPIEndpoints(unittest.TestCase):
    """Basic API endpoint tests for Part 2."""

    def setUp(self):
        """Create test client and reset in-memory repositories."""
        self.app = create_app()
        self.client = self.app.test_client()
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear()

    def test_create_user_success(self):
        """POST /users returns 201 for valid payload."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@gmail.com'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['email'], 'john.doe@gmail.com')

    def test_create_user_duplicate_email(self):
        """POST /users returns 400 when email already exists."""
        payload = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@gmail.com'
        }
        first = self.client.post('/api/v1/users/', json=payload)
        second = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 400)

    def test_create_place_success(self):
        """POST /places returns 201 with valid owner and amenities IDs."""
        user_resp = self.client.post('/api/v1/users/', json={
            'first_name': 'Owner',
            'last_name': 'One',
            'email': 'owner.one@gmail.com'
        })
        amenity_resp = self.client.post('/api/v1/amenities/', json={
            'name': 'WiFi'
        })

        owner_id = user_resp.get_json()['id']
        amenity_id = amenity_resp.get_json()['id']

        place_resp = self.client.post('/api/v1/places/', json={
            'title': 'Cozy Apartment',
            'description': 'Nice place',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': owner_id,
            'amenities': [amenity_id]
        })

        self.assertEqual(place_resp.status_code, 201)
        place_data = place_resp.get_json()
        self.assertEqual(place_data['owner_id'], owner_id)
        self.assertEqual(place_data['amenities'], [amenity_id])

    def test_create_review_and_get_place_reviews(self):
        """POST /reviews then GET /places/<id>/reviews works."""
        user_resp = self.client.post('/api/v1/users/', json={
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@gmail.com'
        })
        amenity_resp = self.client.post('/api/v1/amenities/', json={
            'name': 'Parking'
        })

        owner_id = user_resp.get_json()['id']
        amenity_id = amenity_resp.get_json()['id']

        place_resp = self.client.post('/api/v1/places/', json={
            'title': 'Flat',
            'description': 'Center city',
            'price': 80.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': owner_id,
            'amenities': [amenity_id]
        })
        place_id = place_resp.get_json()['id']

        review_resp = self.client.post('/api/v1/reviews/', json={
            'text': 'Great stay',
            'rating': 5,
            'user_id': owner_id,
            'place_id': place_id
        })

        self.assertEqual(review_resp.status_code, 201)

        place_reviews_resp = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(place_reviews_resp.status_code, 200)
        place_reviews = place_reviews_resp.get_json()
        self.assertEqual(len(place_reviews), 1)
        self.assertEqual(place_reviews[0]['rating'], 5)


if __name__ == '__main__':
    unittest.main()
