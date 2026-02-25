from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = self.text_verif(text)

    @staticmethod
    def text_verif(text):
        if not isinstance(text, str):
            raise TypeError("Review text must be a string.")
        text = text.strip()
        if text == "":
            raise ValueError("Review text cannot be empty.")
        return text

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        self._rating = self.rating_verif(rating)

    @staticmethod
    def rating_verif(rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place):
        self._place = self.place_verif(place)

    @staticmethod
    def place_verif(place):
        if not isinstance(place, Place):
            raise TypeError("Place is required.")
        return place

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = self.user_verif(user)

    @staticmethod
    def user_verif(user):
        if not isinstance(user, User):
            raise TypeError("User is required.")
        return user
