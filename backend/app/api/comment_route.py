from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from app.services.comment_services import (
    create_comment, update_comment, delete_comment,
    get_comment_by_id, get_comments_for_post, get_comments_by_user
)
from app.schemas.comment_sc import CommentGetSchema, CommentPostSchema, UpdateCommentSchema

comment_bp = Blueprint('comment', __name__)

# Create a comment
@comment_bp.route('/comments', methods=['POST'])
@jwt_required()
def create_new_comment():
    try:
        current_user_id = get_jwt_identity()
        schema = CommentPostSchema()
        data = schema.load(request.get_json())
        comment = create_comment(current_user_id, data)
        return jsonify(CommentGetSchema().dump(comment)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 409

# Get a comment by ID
@comment_bp.route('/comments/<string:comment_id>', methods=['GET'])
@jwt_required()
def get_single_comment(comment_id):
    try:
        comment = get_comment_by_id(comment_id)
        return jsonify(CommentGetSchema().dump(comment)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Get all comments for a post
@comment_bp.route('/posts/<string:post_id>/comments', methods=['GET'])
@jwt_required()
def get_post_comments(post_id):
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    try:
        comments = get_comments_for_post(post_id, limit, offset)
        return jsonify(CommentGetSchema(many=True).dump(comments)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Get all comments by a user
@comment_bp.route('/users/comments', methods=['GET'])
@jwt_required()
def get_user_comments():
    current_user_id = get_jwt_identity()
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    try:
        comments = get_comments_by_user(current_user_id, limit, offset)
        return jsonify(CommentGetSchema(many=True).dump(comments)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Update a comment
@comment_bp.route('/comments/<string:comment_id>', methods=['PUT'])
@jwt_required()
def update_existing_comment(comment_id):
    try:
        schema = UpdateCommentSchema()  # Using the new schema
        data = schema.load(request.get_json())
        comment = update_comment(comment_id, data)
        return jsonify(CommentGetSchema().dump(comment)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Delete a comment
@comment_bp.route('/comments/<string:comment_id>', methods=['DELETE'])
@jwt_required()
def remove_comment(comment_id):
    try:
        message = delete_comment(comment_id)
        return jsonify(message), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
