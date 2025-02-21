import uuid
from app import db
from app.models.admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
import random

# In-memory storage for OTPs (For real apps, use a database or Redis)
otp_store = {}

def register_admin(data):
    """Register a new admin"""
    hashed_password = generate_password_hash(data["admin_password"])

    new_admin = Admin(
        admin_id=str(uuid.uuid4()),
        admin_username=data["admin_username"],
        admin_email=data["admin_email"],
        password=hashed_password
    )

    try:
        db.session.add(new_admin)
        db.session.commit()
        return new_admin
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Username or email already exists")

def login_admin(data):
    """Login admin and generate JWT token"""
    admin = Admin.query.filter_by(admin_email=data["admin_email"]).first()

    if not admin or not check_password_hash(admin.password, data["admin_password"]):
        raise ValueError("Invalid email or password")

    token = create_access_token(identity=admin.admin_id)
    return token

def send_otp(admin_email):
    """Generate and store OTP"""
    admin = Admin.query.filter_by(admin_email=admin_email).first()
    if not admin:
        raise ValueError("Email not registered")

    otp = random.randint(100000, 999999)
    otp_store[admin_email] = otp  # Store OTP (should use Redis or DB in production)
    return otp  # In production, send this via email

def verify_otp(admin_email, otp):
    """Verify OTP"""
    if otp_store.get(admin_email) == otp:
        del otp_store[admin_email]  # Remove OTP after successful verification
        return True
    return False

def change_password(admin_id, data):
    """Change admin password"""
    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if not admin:
        raise ValueError("Admin not found")

    if not check_password_hash(admin.password, data["current_password"]):
        raise ValueError("Current password is incorrect")

    if data["new_password"] != data["confirm_password"]:
        raise ValueError("New password and confirm password do not match")

    admin.password = generate_password_hash(data["new_password"])

    try:
        db.session.commit()
        return {"message": "Password changed successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error changing password")

def forget_password(admin_email, data):
    """Reset forgotten password"""
    admin = Admin.query.filter_by(admin_email=admin_email).first()
    if not admin:
        raise ValueError("Email not registered")

    if data["new_password"] != data["confirm_password"]:
        raise ValueError("New password and confirm password do not match")

    admin.password = generate_password_hash(data["new_password"])

    try:
        db.session.commit()
        return {"message": "Password reset successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error resetting password")
