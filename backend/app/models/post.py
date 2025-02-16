import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "post"

    post_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(255), unique=True)
    post_caption = db.Column(db.String(255), nullable=True)
    post_image = db.Column(db.String(255), nullable=True)
    like_count = db.Column(db.String(255), nullable=True)
    comment_count = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.now(), onupdate=func.now())
    is_deleted = db.Column(db.Boolean, default=False)
    
    user = relationship("user", backref=db.backref("post", cascade="all, delete-orphan"))
