#!/usr/bin/python3

from BaseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.verify_len(name)

    def verify_len(name):
        if len(name) < 50:
            return name
        else:
            raise ValueError("Amenity name cannot exceed 50 characters")
