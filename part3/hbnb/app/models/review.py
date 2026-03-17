from app import db
from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    """Review entity linked to a place and a user."""

    __tablename__ = 'reviews'

    _text = db.Column(
        db.String(2000),
        nullable=True)
    
    _rating = db.Column(
        db.Integer,
        nullable=False)

    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id"),
        nullable=False)

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False)

    place = db.relationship(
        "Place",
        back_populates="reviews",
        lazy="select")

    user = db.relationship(
        "User",
        back_populates="reviews",
        lazy="select")


    def __init__(self, text, rating, place, user):
        """Create a review instance."""
        super().__init__()
        self.text = text
        self.rating = rating
        if not isinstance(place, Place):
            raise TypeError("Place is required.")
        if not isinstance(user, User):
            raise TypeError("User is required.")
        self.place = place
        self.user = user


#region Text
    @property
    def text(self):
        """Return the review text."""
        return self._text

    @text.setter
    def text(self, text):
        """Set and validate review text."""
        if text is None:
            self._text = None
            return
        if not isinstance(text, str):
            raise TypeError("Review text must be a string.")
        if len(text) > 2000:
            raise ValueError("Review text cannot exceed 2000 characters.")
        self._text = text
#endregion


#region Rating
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
#endregion


