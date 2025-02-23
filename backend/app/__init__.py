from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from app.config import Config
from flask_cors import CORS



db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    CORS(app)  # Allow cross-origin requests

    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
