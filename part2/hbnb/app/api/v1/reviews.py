from base_model import BaseModel
from places import Place
from users import Users


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.text_verif(text)
        self.rating = self.rating_verif(rating)
        self.place = self.place_verif(place)
        self.user = self.user_verif(user)

    def text_verif(self, text):
        if not isinstance(text, str):
            raise ValueError("Review text must be a string.")
        text = text.strip()
        if text == "":
            raise ValueError("Review text cannot be empty.")
        return text

    def rating_verif(self, rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    def place_verif(self, place):
        if not isinstance(place, Place):
            raise ValueError("Place is required.")
        return place

    def user_verif(self, user):
        if not isinstance(user, Users):
            raise ValueError("User is required.")
        return user
