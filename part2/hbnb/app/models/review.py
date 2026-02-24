from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.text_verif(text)
        self.rating = self.rating_verif(rating)
        self.place = self.place_verif(place)
        self.user = self.user_verif(user)

    @staticmethod
    def text_verif(text):
        if not isinstance(text, str):
            raise TypeError("Review text must be a string.")
        text = text.strip()
        if text == "":
            raise ValueError("Review text cannot be empty.")
        return text

    @staticmethod
    def rating_verif(rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    @staticmethod
    def place_verif(place):
        if not isinstance(place, Place):
            raise TypeError("Place is required.")
        return place

    @staticmethod
    def user_verif(user):
        if not isinstance(user, User):
            raise TypeError("User is required.")
        return user
