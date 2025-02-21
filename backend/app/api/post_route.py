from flask import Blueprint, request, jsonify
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_services import (
    create_post, get_all_posts_by_user, update_post, delete_post, get_post_by_id, get_all_posts
)
from app.schemas.post_sc import PostGetSchema, PostPostSchema

post_bp = Blueprint('post', __name__)

# Create a post
@post_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_new_post():
    try:
        current_user = get_jwt_identity()
        schema = PostPostSchema()
        data = schema.load(request.get_json())
        post = create_post(current_user, data)
        return jsonify(PostGetSchema().dump(post)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 409


# Update a post
@post_bp.route('/posts/<string:post_id>', methods=['PUT'])
@jwt_required()
def update_existing_post(post_id):
    try:
        current_user = get_jwt_identity()
        schema = PostPostSchema(partial=True)
        data = schema.load(request.get_json())
        post = update_post(post_id, data)
        return jsonify(PostGetSchema().dump(post)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Delete a post
@post_bp.route('/posts/<string:post_id>', methods=['DELETE'])
@jwt_required()
def remove_post(post_id):
    try:
        current_user = get_jwt_identity()
        message = delete_post(post_id)
        return jsonify({"message": message}), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Get a single post by ID
@post_bp.route('/posts/<string:post_id>', methods=['GET'])
@jwt_required()
def get_single_post(post_id):
    try:
        current_user = get_jwt_identity()
        post = get_post_by_id(post_id)
        return jsonify(PostGetSchema().dump(post)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Get all posts by a specific user
@post_bp.route('/posts/user/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user_posts(user_id):
    try:
        current_user = get_jwt_identity()

        # Ensure user is requesting their own posts
        if current_user != user_id:
            return jsonify({"error": "Unauthorized access"}), 403

        posts = get_all_posts_by_user(user_id)
        return jsonify(PostGetSchema(many=True).dump(posts)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Get all posts with pagination
@post_bp.route('/posts/all', methods=['GET'])
@jwt_required()
def get_posts():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    posts = get_all_posts(limit, offset)
    return jsonify(PostGetSchema(many=True).dump(posts)), 200
