import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Event(db.Model):
    __tablename__ = "event"

    event_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_fid = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)  
    event = db.Column(db.Text, nullable=False)  
    comment = db.Column(db.Text, nullable=True)  
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())  
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())  
    is_active = db.Column(db.Boolean, default=True, nullable=False)  


    user = relationship("User", backref=db.backref("events", cascade="all, delete-orphan"))
