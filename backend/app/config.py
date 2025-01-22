import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for Flask app.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.urandom(24).hex())
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+mysqlconnector://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ACCESS_TOKEN_EXPIRATION = os.getenv('ACCESS_TOKEN_EXPIRATION')
    REFRESH_TOKEN_EXPIRATION = os.getenv('REFRESH_TOKEN_EXPIRATION')
