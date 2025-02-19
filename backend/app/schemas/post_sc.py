from marshmallow import fields,validate
from app import ma

class PostGetSchema(ma.Schema):
    post_id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    post_caption = fields.String()
    post_image = fields.String()
    like_count = fields.String()
    comment_count = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_deleted = fields.Boolean()


class PostPostSchema(ma.Schema):
    user_id = fields.String(required=True)
    post_caption = fields.String(
        validate=validate.Length(max=50),
        error_messages={"required": "caption is to long"}
    )
    post_image = fields.String()
    like_count = fields.String()
    comment_count = fields.String()
    is_deleted = fields.Boolean()

