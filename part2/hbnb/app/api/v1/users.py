from base_model import BaseModel
from email_validator import validate_email, EmailNotValidError

class Users(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self.first_name_verif(first_name)
        self.last_name = self.last_name_verif(last_name)
        self.email = self.email_verif(email)
        self.password = password
        self.is_admin = is_admin

    def first_name_verif(self, first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string. ")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        return first_name

    def last_name_verif(self, last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string.")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        return last_name

    def email_verif(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        try:
            validate_email(email)
        except EmailNotValidError:
            raise TypeError("Invalid email address format.")
        # - A faire, vérifier que dans la data base l'adresse mail n'existe pas - #
        return email
    