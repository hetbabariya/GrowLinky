import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_sid = db.Column(db.String(255), nullable=True, unique=True)
    user_fid = db.Column(db.String(255), nullable=True, unique=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    user_email = db.Column(db.String(255), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.now(), onupdate=func.now())
    is_valid = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    otp = relationship("Otp", backref="user", lazy=True , cascade="all, delete-orphan")
