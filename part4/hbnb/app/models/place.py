from app import db
from decimal import Decimal, InvalidOperation
from app.models.base_model import BaseModel
from app.models.user import User
from sqlalchemy.orm import relationship


place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey(
        "places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey(
        "amenities.id"), primary_key=True)
)


class Place(BaseModel):
    """Place entity with location, owner, and relations."""

    __tablename__ = 'places'

    _title = db.Column(
        db.String(100),
        nullable=False)

    _description = db.Column(
        db.String(2000),
        nullable=False)

    _price = db.Column(
        db.Numeric(10, 2),
        nullable=False)

    _latitude = db.Column(
        db.Float,
        nullable=False)

    _longitude = db.Column(
        db.Float,
        nullable=False)

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False)

    owner = db.relationship(
        "User",
        back_populates="places",
        lazy="select")

    reviews = db.relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan",
        lazy="select")

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
        lazy="select")

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Create a place instance."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User.")
        self.owner = owner


# region Title

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
# endregion


# region Description

    @property
    def description(self):
        """Return the place description."""
        return self._description

    @description.setter
    def description(self, description):
        """Set and validate the place description."""
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        description = description.strip()
        if not description:
            raise ValueError("Description cannot be empty.")
        if len(description) > 2000:
            raise ValueError("Description cannot exceed 2000 characters.")
        self._description = description
# endregion


# region Price

    @property
    def price(self):
        """Return the nightly price."""
        return self._price

    @price.setter
    def price(self, price):
        """Set and validate the nightly price."""
        try:
            price = Decimal(str(price)).quantize(Decimal('0.01'))
        except (InvalidOperation, TypeError):
            raise TypeError("Price must be a valid number.")
        if price <= 0:
            raise ValueError("Price must be positive.")
        if price > Decimal('99999999.99'):
            raise ValueError("Price exceeds maximum allowed value.")
        self._price = price
# endregion


# region Latitude

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
# endregion


# region Longitude

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
# endregion

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
