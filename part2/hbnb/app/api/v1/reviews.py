from BaseModel import BaseModel


class Users(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user = self._validate_user(user)

    def _validate_text(self, text):
        if not isinstance(text, str):
            raise ValueError("Review text must be a string")
        text = text.strip()
        if text == "":
            raise ValueError("Review text cannot be empty")
        return text

    def _validate_rating(self, rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer")
        if rating < 1 or rating < 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def _validate_place(self, place):
        if place is None:
            raise ValueError("Place is required")
        return place

    def _validate_user(self, user):
        if user is None:
            raise ValueError("User is required")
        return user
