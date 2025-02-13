from flask import Blueprint
from app.api.user_auth_route import auth_bp
from app.api.user_profile_route import profile_bp

# Create a blueprint
api_bp = Blueprint('api', __name__)

# Register sub-blueprints to the main api blueprint
api_bp.register_blueprint(auth_bp,url_prefix='/auth')
api_bp.register_blueprint(profile_bp)