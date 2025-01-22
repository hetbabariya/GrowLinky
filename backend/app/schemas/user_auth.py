from marshmallow import fields, validate, ValidationError
from app import ma

# Reusable password field with validation
def password_field():
    return fields.String(
        required=True,
        validate=validate.Length(min=8, max=15),
        error_messages={"required": "Password is required"}
    )

# Registration Schema
class RegistrationSchema(ma.Schema):
    user_name = fields.String(
        required=True,
        validate=validate.Length(min=5, max=15),
        error_messages={"required": "User name is required"}
    )
    user_email = fields.Email(
        required=True,
        error_messages={"required": "Email is required"}
    )
    user_password = password_field()
    user_fid = fields.String(
        required=False,
        validate=validate.Length(equal=9),
        error_messages={"invalid": "User FID must be 9 characters"}
    )
    user_sid = fields.String(
        required=False,
        validate=validate.Length(equal=9),
        error_messages={"invalid": "User SID must be 9 characters"}
    )

# Login Schema
class LoginSchema(ma.Schema):
    user_email = fields.Email(
        required=True,
        error_messages={"required": "Email is required"}
    )
    user_password = password_field()

# OTP Schema
class OTPSchema(ma.Schema):
    otp = fields.Integer(
        required=True,
        validate=validate.Range(min=100000, max=999999),
        error_messages={"required": "OTP is required", "invalid": "OTP must be a 6-digit number"}
    )

# Email Verification Schema
class EmailVerificationSchema(ma.Schema):
    user_email = fields.Email(
        required=True,
        error_messages={"required": "Email is required"}
    )

# Change Password Schema
class ChangePasswordSchema(ma.Schema):
    current_password = password_field()
    new_password = password_field()
    confirm_password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=15),
        error_messages={"required": "Confirm password is required"}
    )

    # Custom validation for matching passwords
    def validate_passwords(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise ValidationError("New password and confirm password do not match.")
        return data

# Forget Password Schema
class ForgetPasswordSchema(ma.Schema):
    new_password = password_field()
    confirm_password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=15),
        error_messages={"required": "Confirm password is required"}
    )

    # Custom validation for matching passwords
    def validate_passwords(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise ValidationError("New password and confirm password do not match.")
        return data
