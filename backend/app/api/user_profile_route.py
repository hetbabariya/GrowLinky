from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.user_profile_services import create_profile, delete_profile, get_profile_by_username, update_profile
from app.schemas.profile_sc import ProfileGetSchema, ProfilePostSchema, ProfilePutSchema

profile_bp = Blueprint('profile', __name__)

# Get Profile By Username
@profile_bp.route('/profile/me', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        profile = get_profile_by_username(user_id)
        schema = ProfileGetSchema()
        return jsonify(schema.dump(profile)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    except Exception as err:
        return jsonify({"error": "Something went wrong"}), 500


# Create Profile endpoint
@profile_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_profile_endpoint():
    try:
        schema = ProfilePostSchema()
        data = schema.load(request.get_json())

        user_id = get_jwt_identity()
        profile = create_profile(user_id ,data)
        response_schema = ProfileGetSchema()
        return jsonify(response_schema.dump(profile)), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as err:
        return jsonify({"error": "Something went wrong"}), 500


# Update Profile endpoint
@profile_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile_endpoint():
    try:
        schema = ProfilePutSchema()
        data = schema.load(request.get_json())

        user_id = get_jwt_identity()
        profile = update_profile(user_id, data)
        response_schema = ProfileGetSchema()
        return jsonify(response_schema.dump(profile)), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    except Exception as err:
        return jsonify({"error": "Something went wrong"}), 500


# Delete Profile Route
@profile_bp.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_profile_endpoint():
    try:
        user_id = get_jwt_identity()
        message = delete_profile(user_id)
        return jsonify(message), 200

    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500