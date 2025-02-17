from marshmallow import fields
from app import ma


class OtpGetSchema(ma.Schema):
    
    otp_id = fields.String(dump_only=True) 
    user_id = fields.String(required=True) 
    otp = fields.Integer(required=True) 
    created_at = fields.DateTime(dump_only=True) 
    updated_at = fields.DateTime(dump_only=True) 

class OtpPostSchema(ma.Schema):
    user_id = fields.String(required=True) 
    otp = fields.Integer(required=True) 
