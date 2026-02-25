from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = bool(is_admin)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = self.first_name_verif(first_name)

    @staticmethod
    def first_name_verif(first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string.")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        return first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = self.last_name_verif(last_name)

    @staticmethod
    def last_name_verif(last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string.")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        return last_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = self.email_verif(email)

    @staticmethod
    def email_verif(email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        try:
            validate_email(email)
        except EmailNotValidError:
            raise TypeError("Invalid email address format.")
        return email
