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
         
	def _validate_rating(self, rating):
		