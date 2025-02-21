from flask import Blueprint
from app.api.user_auth_route import auth_bp
from app.api.user_profile_route import profile_bp
from app.api.post_route import post_bp
from app.api.like_route import like_bp
from app.api.comment_route import comment_bp
from app.api.admin_route import admin_bp
from app.api.event_route import event_bp
from app.api.request_route import request_bp
from app.api.connection_route import connection_bp

# Create a blueprint
api_bp = Blueprint('api', __name__)

# Register sub-blueprints to the main api blueprint
api_bp.register_blueprint(auth_bp,url_prefix='/auth')
api_bp.register_blueprint(profile_bp)
api_bp.register_blueprint(like_bp)
api_bp.register_blueprint(post_bp)
api_bp.register_blueprint(comment_bp)
api_bp.register_blueprint(admin_bp)
api_bp.register_blueprint(connection_bp)
api_bp.register_blueprint(event_bp)
api_bp.register_blueprint(request_bp)