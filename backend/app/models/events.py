import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "event"

    event_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_fid = db.Column(db.String(255),unique=True)
    event = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.now(), onupdate=func.now())
    created_at = db.Column(db.DateTime, nullable=True )
    is_active = db.Column(db.Boolean, default=True)
    
    user = relationship("user", backref=db.backref("event", cascade="all, delete-orphan"))
