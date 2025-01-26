import os
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from datetime import timedelta


load_dotenv()

def create_user_tokens(user_id):
    """Generate access and refresh tokens"""
    access_token_exp = int(os.getenv('ACCESS_TOKEN_EXPIRATION'))
    refresh_token_exp = int(os.getenv('REFRESH_TOKEN_EXPIRATION'))

    access_token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(minutes=access_token_exp)
    )
    refresh_token = create_refresh_token(
        identity=user_id,
        expires_delta=timedelta(minutes=refresh_token_exp)
    )
    return access_token, refresh_token

def refresh_tokens(refresh_token):
    """Refresh the access token using the refresh token"""
    # If valid refresh token, create new access token

    access_token_exp = int(os.getenv('ACCESS_TOKEN_EXPIRATION'))

    return create_access_token(
        identity=get_jwt_identity(),
        expires_delta=timedelta(minutes=access_token_exp)
    )