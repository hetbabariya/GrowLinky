from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.like_services import (
    create_like, delete_like, get_likes_for_post, get_like_by_id
)
from app.schemas.like_sc import LikeGetSchema

like_bp = Blueprint('like', __name__)

# Like a post
@like_bp.route('/likes', methods=['POST'])
@jwt_required()
def like_post():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        post_id = data.get("post_id")

        if not post_id:
            return jsonify({"error": "Post ID is required"}), 400

        like = create_like(current_user_id, post_id)
        return jsonify(LikeGetSchema().dump(like)), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 409

# Unlike a post
@like_bp.route('/likes', methods=['DELETE'])
@jwt_required()
def unlike_post():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        post_id = data.get("post_id")

        if not post_id:
            return jsonify({"error": "Post ID is required"}), 400

        message = delete_like(current_user_id, post_id)
        return jsonify(message), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Get likes for a post
@like_bp.route('/posts/<string:post_id>/likes', methods=['GET'])
@jwt_required()
def get_post_likes(post_id):
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    try:
        likes = get_likes_for_post(post_id, limit, offset)
        return jsonify(LikeGetSchema(many=True).dump(likes)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Get like by ID
@like_bp.route('/likes/<string:like_id>', methods=['GET'])
@jwt_required()
def get_like(like_id):
    try:
        like = get_like_by_id(like_id)
        return jsonify(LikeGetSchema().dump(like)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
