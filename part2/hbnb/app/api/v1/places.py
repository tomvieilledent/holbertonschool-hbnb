from base_model import BaseModel
from users import Users

from users import Users

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
    
    def title_verif(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return title

    def description_verif(self, description):
        if description:
            if not isinstance(description, str):
                raise TypeError("Description must be a string.")
            return description
        
    def price_verif(self, price):
        if not isinstance(price, float):
            raise TypeError("Price must be a float.")
        if price < 0:
            raise ValueError("Price must be positive.")
    
    def latitude_verif(self, latitude):
        if not isinstance(latitude, float):
            raise TypeError("Latitude must be a float.")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be in range -90 : 90.")
        
    def longitude_verif(self, longitude):
        if not isinstance(longitude, float):
            raise TypeError("Longitude must be a float.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be in range -180 : 180.")
        
    def owner_verif(self, owner):
        if not isinstance(owner, Users):
            raise TypeError("Owner must be an user")

    def title_verif(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters.")
        return title

    def description_verif(self, description):
        if description:
            if not isinstance(description, str):
                raise TypeError("Description must be a string.")
            return description

    def price_verif(self, price):
        if not isinstance(price, float):
            raise TypeError("Price must be a float.")
        if price < 0:
            raise ValueError("Price must be positive.")
        return price

    def latitude_verif(self, latitude):
        if not isinstance(latitude, float):
            raise TypeError("Latitude must be a float.")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be in range -90 : 90.")
        return latitude

    def longitude_verif(self, longitude):
        if not isinstance(longitude, float):
            raise TypeError("Longitude must be a float.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be in range -180 : 180.")
        return longitude

    def owner_verif(self, owner):
        if not isinstance(owner, Users):
            raise TypeError("Owner must be an user.")
        return owner

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
