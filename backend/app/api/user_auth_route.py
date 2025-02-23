from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.user_auth import RegistrationSchema, LoginSchema, OTPSchema, ChangePasswordSchema, ForgetPasswordSchema, UserGetSchema
from app.services.user_auth_services import (
    get_user_by_id, register_user, login_user, generate_otp, verify_otp, forget_password,
    reset_password, change_password, deactivate_account
)
from flask_jwt_extended import get_jwt_identity, jwt_required

auth_bp = Blueprint('auth', __name__)

# Register User
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



# Login User
@auth_bp.route('/login', methods=['POST'])
def login():
    print("Login route called")  # Debugging line
    try:
        schema = LoginSchema()
        data = schema.load(request.get_json())
        print(f"Received data: {data}")  # Debugging line
        tokens = login_user(data)
        return jsonify(tokens), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 401


# Send OTP Route
@auth_bp.route("/send-otp", methods=["POST"])
def send_otp():
    try:
        user_email = request.json.get("user_email")
        generate_otp(user_email)
        return jsonify({"message": "OTP sent successfully"}), 200

    except ValueError as err:
        return jsonify({"error": str(err)}), 400



# Verify OTP Route
@auth_bp.route("/verify-otp", methods=["POST"])
def verify():
    try:
        schema = OTPSchema()
        data = schema.load(request.get_json())

        verify_otp(data["user_email"], data["otp"])
        return jsonify({"message": "OTP verified successfully"}), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400



# Forget Password Route (Send OTP)
@auth_bp.route("/forget-password", methods=["POST"])
def forget():
    try:
        user_email = request.json.get("user_email")
        forget_password(user_email)
        return jsonify({"message": "OTP sent for password reset"}), 200

    except ValueError as err:
        return jsonify({"error": str(err)}), 400

# Reset Password Route
@auth_bp.route("/reset-password", methods=["POST"])
def reset():
    try:
        schema = ForgetPasswordSchema()
        data = schema.load(request.get_json())

        reset_password(data["user_email"], data["new_password"])
        return jsonify({"message": "Password reset successful"}), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

# Change Password Route
@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change():
    try:
        schema = ChangePasswordSchema()
        data = schema.load(request.get_json())

        user_id = get_jwt_identity()
        change_password(user_id, data["current_password"], data["new_password"])
        return jsonify({"message": "Password changed successfully"}), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

# Deactivate Account Route
@auth_bp.route("/deactivate", methods=["POST"])
@jwt_required()
def deactivate():
    try:
        user_id = get_jwt_identity()
        deactivate_account(user_id)
        return jsonify({"message": "Account deactivated"}), 200

    except ValueError as err:
        return jsonify({"error": str(err)}), 400


# Get User by id
@auth_bp.route('/users/<string:user_id>', methods=['GET'])
@jwt_required()
def get_single_user(user_id):
    try:
        current_user = get_jwt_identity()
        user = get_user_by_id(user_id)
        return jsonify(UserGetSchema().dump(user)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Get User by id
@auth_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_user():
    try:
        current_user = get_jwt_identity()
        user = get_user_by_id(current_user)
        return jsonify(UserGetSchema().dump(user)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
