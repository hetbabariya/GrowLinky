from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
from app.utils.user_auth_helper import create_user_tokens

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

def login_user(data):
    user = User.query.filter_by(user_email=data['user_email']).first()

    if not user or not check_password_hash(user.user_password, data['user_password']):
        raise ValueError("Invalid credentials")

    access_token, refresh_token = create_user_tokens(user.user_id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }