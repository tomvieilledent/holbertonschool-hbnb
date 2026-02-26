#!/usr/bin/python3
"""
Comprehensive unit tests for HBnB API endpoints.
Tests all CRUD operations and validation for Users, Amenities, Places, and Reviews.
"""
import unittest
import uuid
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Test suite for User API endpoints."""

    def setUp(self):
        """Initialize test client and create test app."""
        self.app = create_app()
        self.client = self.app.test_client()

    # CREATE (POST) Tests
    def test_create_user_valid(self):
        """Test user creation with valid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], "John")
        self.assertEqual(data['last_name'], "Doe")

    def test_create_user_missing_first_name(self):
        """Test user creation fails without first name."""
        response = self.client.post('/api/v1/users/', json={
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_last_name(self):
        """Test user creation fails without last name."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_email(self):
        """Test user creation fails without email."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_first_name(self):
        """Test user creation fails with empty first name."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_last_name(self):
        """Test user creation fails with empty last name."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_email(self):
        """Test user creation fails with empty email."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        """Test user creation fails with invalid email format."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test user creation fails with duplicate email."""
        email = f"duplicate.{uuid.uuid4()}@example.com"
        # Create first user
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email
        })
        # Try to create second user with same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": email
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_first_name_too_long(self):
        """Test user creation fails with first name exceeding 50 characters."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "a" * 51,
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_last_name_too_long(self):
        """Test user creation fails with last name exceeding 50 characters."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "b" * 51,
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    # GET (Retrieve) Tests
    def test_get_all_users(self):
        """Test retrieving all users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test retrieving a specific user by ID."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": f"alice.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Alice")
        self.assertEqual(data['last_name'], "Smith")

    def test_get_nonexistent_user(self):
        """Test retrieving a nonexistent user returns 404."""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # UPDATE (PUT) Tests
    def test_update_user_first_name(self):
        """Test updating user's first name."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Update first name
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Jonathan"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Jonathan")

    def test_update_user_email(self):
        """Test updating user's email."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Update email
        new_email = f"newemail.{uuid.uuid4()}@example.com"
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "email": new_email
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], new_email)

    def test_update_user_with_invalid_email(self):
        """Test updating user fails with invalid email."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Try to update with invalid email
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)


class TestAmenityEndpoints(unittest.TestCase):
    """Test suite for Amenity API endpoints."""

    def setUp(self):
        """Initialize test client and create test app."""
        self.app = create_app()
        self.client = self.app.test_client()

    # CREATE (POST) Tests
    def test_create_amenity_valid(self):
        """Test amenity creation with valid data."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": f"WiFi-{uuid.uuid4()}"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertIn('WiFi', data['name'])

    def test_create_amenity_missing_name(self):
        """Test amenity creation fails without name."""
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_empty_name(self):
        """Test amenity creation fails with empty name."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_name_too_long(self):
        """Test amenity creation fails with name exceeding 128 characters."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "a" * 129
        })
        self.assertEqual(response.status_code, 400)

    # GET (Retrieve) Tests
    def test_get_all_amenities(self):
        """Test retrieving all amenities."""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_amenity_by_id(self):
        """Test retrieving a specific amenity by ID."""
        # Create an amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": f"Pool-{uuid.uuid4()}"
        })
        amenity_id = create_response.get_json()['id']

        # Get the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Pool', data['name'])

    def test_get_nonexistent_amenity(self):
        """Test retrieving a nonexistent amenity returns 404."""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # UPDATE (PUT) Tests
    def test_update_amenity_name(self):
        """Test updating amenity's name."""
        # Create an amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": f"OldName-{uuid.uuid4()}"
        })
        amenity_id = create_response.get_json()['id']

        # Update name
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "New Amenity Name"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], "New Amenity Name")

    def test_update_amenity_empty_name(self):
        """Test updating amenity fails with empty name."""
        # Create an amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": f"OldName-{uuid.uuid4()}"
        })
        amenity_id = create_response.get_json()['id']

        # Try to update with empty name
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)


class TestPlaceEndpoints(unittest.TestCase):
    """Test suite for Place API endpoints."""

    def setUp(self):
        """Initialize test client and create test app with a user."""
        self.app = create_app()
        self.client = self.app.test_client()
        # Create a user to be the owner
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": f"owner.{uuid.uuid4()}@example.com"
        })
        self.user_id = response.get_json()['id']

    # CREATE (POST) Tests
    def test_create_place_valid(self):
        """Test place creation with valid data."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], "Cozy Apartment")
        self.assertEqual(data['price'], 100.0)

    def test_create_place_missing_title(self):
        """Test place creation fails without title."""
        response = self.client.post('/api/v1/places/', json={
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_empty_title(self):
        """Test place creation fails with empty title."""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_missing_price(self):
        """Test place creation fails without price."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        """Test place creation fails with negative price."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": -50,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test place creation fails with invalid latitude."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 100,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test place creation fails with invalid longitude."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -200,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_missing_owner_id(self):
        """Test place creation fails without owner_id."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194
        })
        self.assertEqual(response.status_code, 400)

    # GET (Retrieve) Tests
    def test_get_all_places(self):
        """Test retrieving all places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        """Test retrieving a specific place by ID."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Test Apartment",
            "price": 120.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Get the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "Test Apartment")

    def test_get_nonexistent_place(self):
        """Test retrieving a nonexistent place returns 404."""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # UPDATE (PUT) Tests
    def test_update_place_title(self):
        """Test updating place's title."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Update title
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "New Title")

    def test_update_place_price(self):
        """Test updating place's price."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Update price
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": 150.0
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['price'], 150.0)

    def test_update_place_invalid_price(self):
        """Test updating place fails with negative price."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Try to update with negative price
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": -50
        })
        self.assertEqual(response.status_code, 400)


class TestReviewEndpoints(unittest.TestCase):
    """Test suite for Review API endpoints."""

    def setUp(self):
        """Initialize test client and create test app with user and place."""
        self.app = create_app()
        self.client = self.app.test_client()
        # Create a user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": f"reviewer.{uuid.uuid4()}@example.com"
        })
        self.user_id = user_response.get_json()['id']

        # Create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 50.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id
        })
        self.place_id = place_response.get_json()['id']

    # CREATE (POST) Tests
    def test_create_review_valid(self):
        """Test review creation with valid data."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], "Great place!")
        self.assertEqual(data['rating'], 5)

    def test_create_review_empty_text(self):
        """Test review creation fails with empty text."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_high(self):
        """Test review creation fails with rating > 5."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_low(self):
        """Test review creation fails with rating < 1."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad place!",
            "rating": 0,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    # GET (Retrieve) Tests
    def test_get_all_reviews(self):
        """Test retrieving all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_review_by_id(self):
        """Test retrieving a specific review by ID."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Excellent place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # Get the review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], "Excellent place!")

    def test_get_nonexistent_review(self):
        """Test retrieving a nonexistent review returns 404."""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        """Test retrieving reviews for a specific place."""
        # Create a review first
        self.client.post('/api/v1/reviews/', json={
            "text": "Good place!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        # Get reviews for this place
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()


class TestUserEndpoints(unittest.TestCase):
    """Test suite for User API endpoints."""

    def setUp(self):
        """Initialize test client and create test app."""
        self.app = create_app()
        self.client = self.app.test_client()

    # CREATE (POST) Tests
    def test_create_user_valid(self):
        """Test user creation with valid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], "John")
        self.assertEqual(data['last_name'], "Doe")

    def test_create_user_missing_first_name(self):
        """Test user creation fails without first name."""
        response = self.client.post('/api/v1/users/', json={
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_last_name(self):
        """Test user creation fails without last name."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_email(self):
        """Test user creation fails without email."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_first_name(self):
        """Test user creation fails with empty first name."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_last_name(self):
        """Test user creation fails with empty last name."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_email(self):
        """Test user creation fails with empty email."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        """Test user creation fails with invalid email format."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test user creation fails with duplicate email."""
        email = f"duplicate.{uuid.uuid4()}@example.com"
        # Create first user
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email
        })
        # Try to create second user with same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": email
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_first_name_too_long(self):
        """Test user creation fails with first name exceeding 50 characters."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "a" * 51,
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_last_name_too_long(self):
        """Test user creation fails with last name exceeding 50 characters."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "b" * 51,
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    # GET (Retrieve) Tests
    def test_get_all_users(self):
        """Test retrieving all users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test retrieving a specific user by ID."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": f"alice.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Alice")
        self.assertEqual(data['last_name'], "Smith")

    def test_get_nonexistent_user(self):
        """Test retrieving a nonexistent user returns 404."""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # UPDATE (PUT) Tests
    def test_update_user_first_name(self):
        """Test updating user's first name."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Update first name
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Jonathan"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Jonathan")

    def test_update_user_email(self):
        """Test updating user's email."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Update email
        new_email = f"newemail.{uuid.uuid4()}@example.com"
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "email": new_email
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], new_email)

    def test_update_user_with_invalid_email(self):
        """Test updating user fails with invalid email."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{uuid.uuid4()}@example.com"
        })
        user_id = create_response.get_json()['id']

        # Try to update with invalid email
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_empty_name(self):
        """Test updating amenity fails with empty name."""
        # Create an amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": f"OldName-{uuid.uuid4()}"
        })
        amenity_id = create_response.get_json()['id']

        # Try to update with empty name
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    # DELETE Tests
    def test_delete_amenity(self):
        """Test deleting an amenity."""
        # Create an amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": f"ToDelete-{uuid.uuid4()}"
        })
        amenity_id = create_response.get_json()['id']

        # Delete the amenity
        response = self.client.delete(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

        # Verify amenity is deleted
        get_response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 404)


class TestPlaceEndpoints(unittest.TestCase):
    """Test suite for Place API endpoints."""

    def setUp(self):
        """Initialize test client and create test app with a user."""
        self.app = create_app()
        self.client = self.app.test_client()
        # Create a user to be the owner
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": f"owner.{uuid.uuid4()}@example.com"
        })
        self.user_id = response.get_json()['id']

    # CREATE (POST) Tests
    def test_create_place_valid(self):
        """Test place creation with valid data."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], "Cozy Apartment")
        self.assertEqual(data['price'], 100.0)

    def test_create_place_missing_title(self):
        """Test place creation fails without title."""
        response = self.client.post('/api/v1/places/', json={
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_empty_title(self):
        """Test place creation fails with empty title."""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_missing_price(self):
        """Test place creation fails without price."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        """Test place creation fails with negative price."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": -50,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test place creation fails with invalid latitude."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 100,  # Out of range (-90 to 90)
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test place creation fails with invalid longitude."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -200,  # Out of range (-180 to 180)
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_missing_owner_id(self):
        """Test place creation fails without owner_id."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_nonexistent_owner(self):
        """Test place creation fails with nonexistent owner."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "nonexistent-owner"
        })
        self.assertEqual(response.status_code, 404)

    # GET (Retrieve) Tests
    def test_get_all_places(self):
        """Test retrieving all places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        """Test retrieving a specific place by ID."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Test Apartment",
            "price": 120.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Get the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "Test Apartment")

    def test_get_nonexistent_place(self):
        """Test retrieving a nonexistent place returns 404."""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # UPDATE (PUT) Tests
    def test_update_place_title(self):
        """Test updating place's title."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Update title
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "New Title")

    def test_update_place_price(self):
        """Test updating place's price."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Update price
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": 150.0
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['price'], 150.0)

    def test_update_place_invalid_price(self):
        """Test updating place fails with negative price."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Try to update with negative price
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": -50
        })
        self.assertEqual(response.status_code, 400)

    # DELETE Tests
    def test_delete_place(self):
        """Test deleting a place."""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "To Delete",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = create_response.get_json()['id']

        # Delete the place
        response = self.client.delete(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)

        # Verify place is deleted
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 404)


class TestReviewEndpoints(unittest.TestCase):
    """Test suite for Review API endpoints."""

    def setUp(self):
        """Initialize test client and create test app with user and place."""
        self.app = create_app()
        self.client = self.app.test_client()
        # Create a user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": f"reviewer.{uuid.uuid4()}@example.com"
        })
        self.user_id = user_response.get_json()['id']

        # Create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 50.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id
        })
        self.place_id = place_response.get_json()['id']

    # CREATE (POST) Tests
    def test_create_review_valid(self):
        """Test review creation with valid data."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], "Great place!")
        self.assertEqual(data['rating'], 5)

    def test_create_review_missing_text(self):
        """Test review creation fails without text."""
        response = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        """Test review creation fails with empty text."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_rating(self):
        """Test review creation fails without rating."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_high(self):
        """Test review creation fails with rating > 5."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_low(self):
        """Test review creation fails with rating < 1."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad place!",
            "rating": 0,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_user_id(self):
        """Test review creation fails without user_id."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_place_id(self):
        """Test review creation fails without place_id."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_nonexistent_user(self):
        """Test review creation fails with nonexistent user."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": "nonexistent-user",
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 404)

    def test_create_review_nonexistent_place(self):
        """Test review creation fails with nonexistent place."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": "nonexistent-place"
        })
        self.assertEqual(response.status_code, 404)

    # GET (Retrieve) Tests
    def test_get_all_reviews(self):
        """Test retrieving all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_review_by_id(self):
        """Test retrieving a specific review by ID."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Excellent place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # Get the review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], "Excellent place!")

    def test_get_nonexistent_review(self):
        """Test retrieving a nonexistent review returns 404."""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        """Test retrieving reviews for a specific place."""
        # Create a review first
        self.client.post('/api/v1/reviews/', json={
            "text": "Good place!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        # Get reviews for this place
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    # UPDATE (PUT) Tests
    def test_update_review_text(self):
        """Test updating review's text."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Original text",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # Update text
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated text"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], "Updated text")

    def test_update_review_rating(self):
        """Test updating review's rating."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Good place!",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # Update rating
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['rating'], 5)

    def test_update_review_invalid_rating(self):
        """Test updating review fails with invalid rating."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Good place!",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # Try to update with invalid rating
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "rating": 10
        })
        self.assertEqual(response.status_code, 400)

    # DELETE Tests
    def test_delete_review(self):
        """Test deleting a review."""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "To delete",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # Delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

        # Verify review is deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
