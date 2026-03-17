import uuid
from datetime import datetime, timezone
from app import db


class BaseModel(db.Model):
    """Base entity with UUID and timestamps."""

    __abstract__ = True

    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()))
    
    created_at = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc))
    
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self):
        """Initialize base fields for a new model instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()