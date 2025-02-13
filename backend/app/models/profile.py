import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Profile(db.Model):
    __tablename__ = "profile"

    profile_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)
    profile_name = db.Column(db.String(255), nullable=False)
    subheading = db.Column(db.String(255))
    skills = db.Column(db.Text)
    bio = db.Column(db.Text)
    gender = db.Column(db.String(50), nullable=False)
    mobile_no = db.Column(db.String(20), nullable=False)
    social_links = db.Column(db.Text)
    experience = db.Column(db.Text)
    dp_link = db.Column(db.String(500))
    post_count = db.Column(db.Integer, default=0)
    connection_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    is_public = db.Column(db.Boolean, default=True)

    user = relationship("User", backref=db.backref("profile", cascade="all, delete-orphan"))
