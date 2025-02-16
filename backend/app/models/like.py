import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "like"

    like_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = db.Column(db.String(255))
    user_id_like = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    
    user = relationship("post", backref=db.backref("like", cascade="all, delete-orphan"))
