import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "connection"

    connection_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id_self = db.Column(db.String(255) )
    user_id_connection = db.Column(db.String(255))
    request_id = db.Column(db.String(255),unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.now(), onupdate=func.now())
    is_active = db.Column(db.Boolean, default=True)
    
    user = relationship("user", backref=db.backref("connection", cascade="all, delete-orphan"))
