from werkzeug.security import generate_password_hash , check_password_hash
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db
from app.utils.user_auth_helper import create_user_tokens

# register user
def register_user(data) :
    existing_user = User.query.filter_by(user_email=data['user_email']).first()

    if existing_user :
        raise ValueError("User with this email already exists.")

    new_user = User(
        user_name = data['user_name'],
        user_email = data['user_email'],
        user_password = generate_password_hash(data['user_password']),
        user_fid=data.get('user_fid'),
        user_sid=data.get('user_sid')
    )

    db.session.add(new_user)
    db.session.commit()

    return new_user

# login user
def login_user(data):
    user = User.query.filter_by(user_email=data['user_email']).first()

    if not user :
        raise ValueError("User with this email does not exist.")

    if user and check_password_hash(user.user_password, data['user_password']):
        access_token, refresh_token = create_user_tokens(user.id)

        # return jsonify({
        #     'access_token': access_token,
        #     'refresh_token': refresh_token
        # }), 200

    else :
        raise ValueError("Invalid credentials")
