import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Otp(db.Model):
    __tablename__ = 'otp'

    otp_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)
    otp = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.now(), onupdate=func.now())

    user = relationship("User", backref=db.backref("otps", cascade="all, delete-orphan"))
