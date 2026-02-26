from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    """Review entity linked to a place and a user."""

    def __init__(self, text, rating, place, user):
        """Create a review instance."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """Return the review text."""
        return self._text

    @text.setter
    def text(self, text):
        """Set and validate review text."""
        if not isinstance(text, str):
            raise TypeError("Review text must be a string.")
        text = text.strip()
        if text == "":
            raise ValueError("Review text cannot be empty.")
        self._text = text

    @property
    def rating(self):
        """Return the review rating."""
        return self._rating

    @rating.setter
    def rating(self, rating):
        """Set and validate review rating."""
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self._rating = rating

    @property
    def place(self):
        """Return the reviewed place."""
        return self._place

    @place.setter
    def place(self, place):
        """Set and validate the reviewed place."""
        if not isinstance(place, Place):
            raise TypeError("Place is required.")
        self._place = place

    @property
    def user(self):
        """Return the review author."""
        return self._user

    @user.setter
    def user(self, user):
        """Set and validate the review author."""
        if not isinstance(user, User):
            raise TypeError("User is required.")
        self._user = user
