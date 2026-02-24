from BaseModel import BaseModel

class Users(BaseModel):
    def __init__(self, first_name, last_name, email, password, admin):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.admin = admin
