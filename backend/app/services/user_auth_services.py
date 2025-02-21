from datetime import datetime, timezone, timedelta
import uuid
import random
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.otp import Otp
from app import db
from app.utils.user_auth_helper import create_user_tokens, send_otp_email
from sqlalchemy.sql import func


# Register User
def register_user(data):
    existing_user = User.query.filter(
        (User.user_email == data['user_email']) |
        (User.user_name == data['user_name'])
    ).first()

    if existing_user:
        raise ValueError("User with this email or username already exists.")

    new_user = User(
        user_name=data['user_name'],
        user_email=data['user_email'],
        user_password=generate_password_hash(data['user_password'], method='pbkdf2:sha256'),
        user_fid=data.get('user_fid'),
        user_sid=data.get('user_sid')
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user



# Login User
def login_user(data):
    user = User.query.filter_by(user_email=data['user_email']).first()

    if not user or not check_password_hash(user.user_password, data['user_password']):
        raise ValueError("Invalid credentials")

    access_token, refresh_token = create_user_tokens(user.user_id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }



# Generate and Send OTP Service
def generate_otp(user_email):
    user = User.query.filter_by(user_email=user_email).first()
    if not user:
        raise ValueError("User not found")

    otp_code = random.randint(100000, 999999)

    otp_entry = Otp(
        otp_id=str(uuid.uuid4()),
        user_id=user.user_id,
        otp=otp_code
    )

    db.session.add(otp_entry)
    db.session.commit()

    # Send OTP via email
    if not send_otp_email(user_email, otp_code):
        raise ValueError("Failed to send OTP email")

    return True




# Verify OTP Service

def verify_otp(user_email, otp_code):
    user = User.query.filter_by(user_email=user_email).first()
    if not user:
        raise ValueError("User not found")

    otp_entry = Otp.query.filter_by(user_id=user.user_id, otp=otp_code).first()
    if not otp_entry:
        raise ValueError("Invalid OTP")


    otp_expiry_time = otp_entry.created_at + timedelta(minutes=2)
    current_time = datetime.now()

    if current_time > otp_expiry_time:
        db.session.delete(otp_entry)  # Delete expired OTP
        db.session.commit()
        raise ValueError("OTP has expired")

    # OTP is valid, delete it and validate user
    db.session.delete(otp_entry)
    db.session.commit()

    user.is_valid = True
    db.session.commit()

    return True




# Forget Password (Send OTP)
def forget_password(user_email):
    return generate_otp(user_email)




# Reset Password Service
def reset_password(user_email, new_password):
    user = User.query.filter_by(user_email=user_email).first()
    if not user:
        raise ValueError("User not found")

    user.user_password = generate_password_hash(new_password)
    db.session.commit()

    return True




# Change Password Service
def change_password(user_id, current_password, new_password):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    if not check_password_hash(user.user_password, current_password):
        raise ValueError("Incorrect current password")

    user.user_password = generate_password_hash(new_password)
    db.session.commit()

    return True



# Deactivate Account Service
def deactivate_account(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    user.is_active = False
    db.session.commit()

    return True