import uuid
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "request"

    request_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id_self = db.Column(db.String(255))
    user_id_connection = db.Column(db.String(255),unique=True)
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    is_accepted=db.column(db.boolean ,default=True)
    
    user = relationship("connection", backref=db.backref("request", cascade="all, delete-orphan"))
