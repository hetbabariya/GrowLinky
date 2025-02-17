from marshmallow import fields, validate, ValidationError
from app import ma 


class CommentGetSchema(ma.Schema):
    comment_id = fields.String(dump_only=True)  
    post_id = fields.String(required=True)  
    user_id = fields.String(required=True)  
    comment_text = fields.String(required=True)  
    created_at = fields.DateTime(dump_only=True)  
    updated_at = fields.DateTime(dump_only=True)  


class CommentPostSchema(ma.Schema):
    post_id = fields.String(required=True)  
    user_id = fields.String(required=True)  
    comment_text = fields.String(
        required=True, 
        validate=validate.Length(min=1, max=500),  
        error_messages={"required": "Comment text is required", "invalid": "Comment text is too long"}
    )
