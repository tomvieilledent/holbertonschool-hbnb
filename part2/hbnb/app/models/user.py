from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    """User entity with identity and email validation."""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Create a user instance."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

    @property
    def first_name(self):
        """Return the user's first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Set and validate the user's first name."""
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string.")
        first_name = first_name.strip()
        if not first_name:
            raise ValueError("First name cannot be empty.")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        self._first_name = first_name

    @property
    def last_name(self):
        """Return the user's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Set and validate the user's last name."""
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string.")
        last_name = last_name.strip()
        if not last_name:
            raise ValueError("Last name cannot be empty.")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        self._last_name = last_name

    @property
    def email(self):
        """Return the user's email."""
        return self._email

    @email.setter
    def email(self, email):
        """Set and validate the user's email."""
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        email = email.strip()
        if not email:
            raise ValueError("Email cannot be empty.")
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            raise TypeError("Invalid email address format.")
        self._email = email
