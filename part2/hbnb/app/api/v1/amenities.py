#!/usr/bin/python3

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name