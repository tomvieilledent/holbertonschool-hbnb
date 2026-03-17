from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Place entity with location, owner, and relations."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Create a place instance."""
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
        """Return the place title."""
        return self._title

    @title.setter
    def title(self, title):
        """Set and validate the place title."""
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters.")
        self._title = title

    @property
    def description(self):
        """Return the place description."""
        return self._description

    @description.setter
    def description(self, description):
        """Set and validate the place description."""
        if description is None:
            self._description = None
            return
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        description = description.strip()
        if not description:
            raise ValueError("Description cannot be empty.")
        self._description = description

    @property
    def price(self):
        """Return the nightly price."""
        return self._price

    @price.setter
    def price(self, price):
        """Set and validate the nightly price."""
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a float.")
        if price < 0:
            raise ValueError("Price must be positive.")
        self._price = float(price)

    @property
    def latitude(self):
        """Return the latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Set and validate latitude coordinates."""
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a float.")
        if not (-90 <= float(latitude) <= 90):
            raise ValueError("Latitude must be in range -90 : 90.")
        self._latitude = float(latitude)

    @property
    def longitude(self):
        """Return the longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Set and validate longitude coordinates."""
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a float.")
        if not (-180 <= float(longitude) <= 180):
            raise ValueError("Longitude must be in range -180 : 180.")
        self._longitude = float(longitude)

    @property
    def owner(self):
        """Return the place owner."""
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Set and validate the place owner."""
        if not isinstance(owner, User):
            raise TypeError("Owner must be an user.")
        self._owner = owner

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
