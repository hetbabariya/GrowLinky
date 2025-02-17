import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Request(db.Model):
    __tablename__ = "request"

    request_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id_self = db.Column(db.String(36), db.ForeignKey('post.post_id'), nullable=False)  # Ensuring proper FK reference
    user_id_connection = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)  # FK to User table
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    is_accepted = db.Column(db.Boolean, default=False)  # Fixing `db.column` typo

    post = relationship("Post", backref=db.backref("requests", cascade="all, delete-orphan"))
    user = relationship("User", backref=db.backref("requests", cascade="all, delete-orphan"))
