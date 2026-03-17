#!/usr/bin/python3

from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity entity for place features."""

    __tablename__ = 'amenities'

    _name = db.Column(
        db.String(50),
        nullable=False)

    places = db.relationship(
        "Place",
        secondary="place_amenity",
        back_populates="amenities",
        lazy="select")


    def __init__(self, name):
        """Create an amenity instance."""
        super().__init__()
        self.name = name


#region Name
    @property
    def name(self):
        """Return the amenity name."""
        return self._name

    @name.setter
    def name(self, name):
        """Set and validate the amenity name."""
        if not isinstance(name, str):
            raise TypeError("Amenity name must be a string.")
        name = name.strip()
        if not name:
            raise ValueError("Amenity name cannot be empty.")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        self._name = name
#endregion