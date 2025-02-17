from marshmallow import fields, validate
from app import ma


def password_field():
    return fields.String(
        required=True,
        validate=validate.Length(min=8, max=15),
        error_messages={"required": "Password is required"}
    )


class AdminRegistrationSchema(ma.Schema):
    admin_username = fields.String(
        required=True,
        validate=validate.Length(min=5, max=15),
        error_messages={"required": "Admin username is required"}
    )
    admin_email = fields.Email(
        required=True,
        error_messages={"required": "Admin email is required"}
    )
    admin_password = password_field()


class AdminLoginSchema(ma.Schema):
    admin_email = fields.Email(
        required=True,
        error_messages={"required": "Email is required"}
    )
    admin_password = password_field()


class AdminOTPSchema(ma.Schema):
    otp = fields.Integer(
        required=True,
        validate=validate.Range(min=100000, max=999999),
        error_messages={"required": "OTP is required", "invalid": "OTP must be a 6-digit number"}
    )


class AdminEmailVerificationSchema(ma.Schema):
    admin_email = fields.Email(
        required=True,
        error_messages={"required": "Email is required"}
    )


class AdminChangePasswordSchema(ma.Schema):
    current_password = password_field()
    new_password = password_field()
    confirm_password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=15),
        error_messages={"required": "Confirm password is required"}
    )


class AdminForgetPasswordSchema(ma.Schema):
    new_password = password_field()
    confirm_password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=15),
        error_messages={"required": "Confirm password is required"}
    )

