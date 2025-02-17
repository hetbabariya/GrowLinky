import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Comment(db.Model):
    __tablename__ = "comment"

    comment_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = db.Column(db.String(255), db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    post = relationship("Post", backref=db.backref("comments", cascade="all, delete-orphan"))
    user = relationship("User", backref=db.backref("comments", cascade="all, delete-orphan"))
