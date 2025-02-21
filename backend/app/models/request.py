import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Request(db.Model):
    __tablename__ = "request"

    request_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id_self = db.Column(db.String(36), db.ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    user_id_connection = db.Column(db.String(36), db.ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    is_accepted = db.Column(db.Boolean, nullable=False, default=False)

    user_self = relationship("User", foreign_keys=[user_id_self], backref=db.backref("sent_requests", cascade="all, delete-orphan"))
    user_connection = relationship("User", foreign_keys=[user_id_connection], backref=db.backref("received_requests", cascade="all, delete-orphan"))
