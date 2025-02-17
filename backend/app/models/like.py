import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Like(db.Model):
    __tablename__ = "like"

    like_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = db.Column(db.String(255), db.ForeignKey('post.post_id'), nullable=False)  
    user_id_like = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)  
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())  
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    post = relationship("Post", backref=db.backref("likes", cascade="all, delete-orphan"))
    user = relationship("User", backref=db.backref("likes", cascade="all, delete-orphan"))
