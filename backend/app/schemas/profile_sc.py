from marshmallow import fields, validate, ValidationError
from app import ma

class ProfileGetSchema(ma.Schema):
    profile_id = fields.String(dump_only=True)  
    user_id = fields.String(required=True)
    profile_name = fields.String(required=True)
    subheading = fields.String()
    skills = fields.String()
    bio = fields.String()
    gender = fields.String(required=True)
    mobile_no = fields.String()
    social_links = fields.String()
    experience = fields.String()
    dp_link = fields.String()
    post_count = fields.Integer(dump_only=True, default=0)
    connection_count = fields.Integer(dump_only=True, default=0)
    view_count = fields.Integer(dump_only=True, default=0)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_public = fields.Boolean()

# Schema for creating a profile (POST request)
class ProfilePostSchema(ma.Schema):
    user_id = fields.String(required=True)
    profile_name = fields.String(
        required=True, 
        validate=validate.Length(min=5, max=15), 
        error_messages={"required": "Profile name is required"}
    )
    subheading = fields.String(
        validate=validate.Length(min=15, max=50), 
        error_messages={"required": "Subheading should be between 15 to 50 characters"}
    )
    skills = fields.String()
    bio = fields.String()
    gender = fields.String(required=True)
    mobile_no = fields.String(
        validate=validate.Length(equal=10), 
        error_messages={"required": "Please enter a valid 10-digit mobile number"}
    )
    social_links = fields.String()
    experience = fields.String(
        validate=validate.Length(min=15, max=50),
        error_messages={"required": "Experience should be between 15 to 50 characters"}
    )
    dp_link = fields.String()
    is_public = fields.Boolean()

# Schema for updating a profile (PUT request)
class ProfilePutSchema(ma.Schema):
    profile_name = fields.String(validate=validate.Length(min=5, max=15))
    subheading = fields.String(validate=validate.Length(min=15, max=50))
    skills = fields.String()
    bio = fields.String()
    gender = fields.String()
    mobile_no = fields.String(validate=validate.Length(equal=10))
    social_links = fields.String()
    experience = fields.String(validate=validate.Length(min=15, max=50))
    dp_link = fields.String()
    is_public = fields.Boolean()
