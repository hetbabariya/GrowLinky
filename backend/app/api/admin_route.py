from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.admin_services import (
    register_admin, login_admin, send_otp, verify_otp, change_password, forget_password
)
from app.schemas.admin_sc import (
    AdminRegistrationSchema, AdminLoginSchema, AdminOTPSchema,
    AdminEmailVerificationSchema, AdminChangePasswordSchema, AdminForgetPasswordSchema
)

admin_bp = Blueprint("admin", __name__)

# Register Admin
@admin_bp.route("/admin/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        schema = AdminRegistrationSchema()
        validated_data = schema.load(data)
        admin = register_admin(validated_data)
        return jsonify({"message": "Admin registered successfully", "admin_id": admin.admin_id}), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 400

# Login Admin
@admin_bp.route("/admin/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        schema = AdminLoginSchema()
        validated_data = schema.load(data)
        token = login_admin(validated_data)
        return jsonify({"access_token": token}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 401

# Send OTP
@admin_bp.route("/admin/send-otp", methods=["POST"])
def send_admin_otp():
    try:
        data = request.get_json()
        schema = AdminEmailVerificationSchema()
        validated_data = schema.load(data)
        otp = send_otp(validated_data["admin_email"])
        return jsonify({"message": "OTP sent successfully", "otp": otp}), 200  # Send OTP via email in real implementation
    except Exception as err:
        return jsonify({"error": str(err)}), 400

# Verify OTP
@admin_bp.route("/admin/verify-otp", methods=["POST"])
def verify_admin_otp():
    try:
        data = request.get_json()
        schema = AdminOTPSchema()
        validated_data = schema.load(data)
        is_verified = verify_otp(validated_data["admin_email"], validated_data["otp"])
        if is_verified:
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"error": "Invalid OTP"}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 400

# Change Password
@admin_bp.route("/admin/change-password", methods=["PUT"])
@jwt_required()
def change_admin_password():
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        schema = AdminChangePasswordSchema()
        validated_data = schema.load(data)
        response = change_password(admin_id, validated_data)
        return jsonify(response), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400

# Forgot Password
@admin_bp.route("/admin/forgot-password", methods=["PUT"])
def forgot_admin_password():
    try:
        data = request.get_json()
        schema = AdminForgetPasswordSchema()
        validated_data = schema.load(data)
        response = forget_password(validated_data["admin_email"], validated_data)
        return jsonify(response), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400
