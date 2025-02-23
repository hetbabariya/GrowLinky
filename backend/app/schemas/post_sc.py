from marshmallow import fields,validate
from app import ma

class PostGetSchema(ma.Schema):
    post_id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    user_name = fields.String(dump_only=True)  # Add user_name field
    post_caption = fields.String()
    post_image = fields.String()
    like_count = fields.Integer()  # Should be Integer instead of String
    comment_count = fields.Integer()  # Should be Integer instead of String
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_deleted = fields.Boolean()


class PostPostSchema(ma.Schema):
    user_id = fields.String()
    post_caption = fields.String(
        validate=validate.Length(max=50),
        error_messages={"required": "caption is to long"}
    )
    post_image = fields.String()
    like_count = fields.String(dump_only=True)
    comment_count = fields.String(dump_only=True)
    is_deleted = fields.Boolean()
