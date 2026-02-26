#!/usr/bin/python3

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity entity for place features."""

    def __init__(self, name):
        """Create an amenity instance."""
        super().__init__()
        self.name = name

    @property
    def name(self):
        """Return the amenity name."""
        return self._name

    @name.setter
    def name(self, name):
        """Set and validate the amenity name."""
        if not isinstance(name, str):
            raise TypeError("Amenity name must be a string.")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        self._name = name
