from BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError

class Users(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self.first_name_verif(first_name)
        self.last_name = self.last_name_verif(last_name)
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def first_name_verif(first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string. ")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        return first_name

    def last_name_verif(last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        return last_name
        
    def email_verif(email):
        if validate_email(email) == False:
            raise TypeError("Invalid email address format.")
        return email