#!/usr/bin/python3

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade for business operations on HBnB entities."""

    def __init__(self):
        """Initialize in-memory repositories for all entities."""
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)


# region Users

    def create_user(self, user_data):
        """Create and store a new user."""
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repository.get_by_attribute('email', email)

    def get_all_users(self):
        """Return all users."""
        return self.user_repository.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user by ID."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        if 'email' in user_data:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
        self.user_repository.update(user_id, user_data)
        return user

# endregion


# region Amenities

    def create_amenity(self, amenity_data):
        """Create and store a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        """Return all amenities."""
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity by ID."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        self.amenity_repository.update(amenity_id, amenity_data)
        return amenity

# endregion


# region Places

    def create_place(self, place_data):
        """Create and store a new place."""
        owner = place_data.get('owner')
        if not owner:
            owner_id = place_data.get('owner_id')
            if not owner_id:
                raise ValueError("Owner is required")
            owner = self.get_user(owner_id)
            if not owner:
                raise ValueError("User not found")

        amenities = []
        for item in place_data.get('amenities', []):
            amenity = item if isinstance(
                item, Amenity) else self.get_amenity(item)
            if not amenity:
                raise ValueError("Amenity not found")
            amenities.append(amenity)

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner,
        )
        place.amenities = amenities
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repository.get(place_id)

    def get_all_places(self):
        """Return all places."""
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place by ID."""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        data = place_data.copy()

        if 'owner_id' in data:
            owner = self.get_user(data['owner_id'])
            if not owner:
                raise ValueError("User not found")
            data['owner'] = owner
            del data['owner_id']

        if 'amenities' in data:
            resolved = []
            for item in data['amenities']:
                amenity = item if isinstance(
                    item, Amenity) else self.get_amenity(item)
                if not amenity:
                    raise ValueError("Amenity not found")
                resolved.append(amenity)
            data['amenities'] = resolved

        self.place_repository.update(place_id, data)
        return place

# endregion


# region Reviews

    def create_review(self, review_data):
        """Create and store a new review."""
        user = review_data.get('user')
        if not user:
            user_id = review_data.get('user_id')
            if not user_id:
                raise ValueError("User is required")
            user = self.get_user(user_id)
            if not user:
                raise ValueError("User not found")

        place = review_data.get('place')
        if not place:
            place_id = review_data.get('place_id')
            if not place_id:
                raise ValueError("Place is required")
            place = self.get_place(place_id)
            if not place:
                raise ValueError("Place not found")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,
            user=user,
        )
        place.add_review(review)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        """Return all reviews."""
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        """Return all reviews linked to a place ID."""
        return [
            review for review in self.review_repository.get_all()
            if review.place and review.place.id == place_id
        ]

    def update_review(self, review_id, review_data):
        """Update an existing review by ID."""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repository.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repository.delete(review_id)

# endregion
