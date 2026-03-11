from app import db
from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError

###Il manque le set_password###

class User(BaseModel):
    """User entity with identity and email validation."""

    __tablename__ = 'users'

    _first_name = db.Column(db.String(50), nullable=False)
    _last_name = db.Column(db.String(50), nullable=False)
    _email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """Create a user instance."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._is_admin = bool(is_admin)
        self._password = ""
        if password:
            self.set_password(password)
    

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
