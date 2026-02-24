from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.title_verif(title)
        self.description = self.description_verif(description)
        self.price = self.price_verif(price)
        self.latitude = self.latitude_verif(latitude)
        self.longitude = self.longitude_verif(longitude)
        self.owner = self.owner_verif(owner)
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @staticmethod
    def title_verif(title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters.")
        return title

    @staticmethod
    def description_verif(description):
        if description is None:
            return None
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        return description

    @staticmethod
    def price_verif(price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a float.")
        if price < 0:
            raise ValueError("Price must be positive.")
        return float(price)

    @staticmethod
    def latitude_verif(latitude):
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a float.")
        if not (-90 <= float(latitude) <= 90):
            raise ValueError("Latitude must be in range -90 : 90.")
        return float(latitude)

    @staticmethod
    def longitude_verif(longitude):
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a float.")
        if not (-180 <= float(longitude) <= 180):
            raise ValueError("Longitude must be in range -180 : 180.")
        return float(longitude)

    @staticmethod
    def owner_verif(owner):
        if not isinstance(owner, User):
            raise TypeError("Owner must be an user.")
        return owner

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
