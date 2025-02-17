import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Connection(db.Model):
    __tablename__ = "connection"

    connection_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id_self = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)
    user_id_connection = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)
    request_id = db.Column(db.String(255), db.ForeignKey('request.request_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


    request = relationship("Request", backref=db.backref("connections", cascade="all, delete-orphan"))
    user_self = relationship("User", foreign_keys=[user_id_self], backref=db.backref("connections_sent", cascade="all, delete-orphan"))
    user_connection = relationship("User", foreign_keys=[user_id_connection], backref=db.backref("connections_received", cascade="all, delete-orphan"))
