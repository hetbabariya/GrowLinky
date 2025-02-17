import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_username = db.Column(db.String(255),unique=True)
    admin_email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255),unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
