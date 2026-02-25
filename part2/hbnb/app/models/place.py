from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = self.title_verif(title)

    @staticmethod
    def title_verif(title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters.")
        return title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = self.description_verif(description)

    @staticmethod
    def description_verif(description):
        if description is None:
            return None
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        return description

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = self.price_verif(price)

    @staticmethod
    def price_verif(price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a float.")
        if price < 0:
            raise ValueError("Price must be positive.")
        return float(price)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = self.latitude_verif(latitude)

    @staticmethod
    def latitude_verif(latitude):
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a float.")
        if not (-90 <= float(latitude) <= 90):
            raise ValueError("Latitude must be in range -90 : 90.")
        return float(latitude)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = self.longitude_verif(longitude)

    @staticmethod
    def longitude_verif(longitude):
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a float.")
        if not (-180 <= float(longitude) <= 180):
            raise ValueError("Longitude must be in range -180 : 180.")
        return float(longitude)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = self.owner_verif(owner)

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
