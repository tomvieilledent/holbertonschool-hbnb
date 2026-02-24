from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self.first_name_verif(first_name)
        self.last_name = self.last_name_verif(last_name)
        self.email = self.email_verif(email)
        self.password = password
        self.is_admin = bool(is_admin)

    @staticmethod
    def first_name_verif(first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string.")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        return first_name

    @staticmethod
    def last_name_verif(last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string.")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        return last_name

    @staticmethod
    def email_verif(email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        try:
            validate_email(email)
        except EmailNotValidError:
            raise TypeError("Invalid email address format.")
        return email
