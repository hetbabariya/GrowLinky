from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.user_auth import RegistrationSchema, LoginSchema
from app.services.user_auth_services import register_user, login_user
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        schema = RegistrationSchema()
        data = schema.load(request.get_json())
        user = register_user(data)
        return jsonify({
            "message": "Registration successful",
            "user": {
                "id": user.user_id,
                "username": user.user_name,
                "email": user.user_email
            }
        }), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        schema = LoginSchema()
        data = schema.load(request.get_json())
        tokens = login_user(data)
        return jsonify(tokens), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 401