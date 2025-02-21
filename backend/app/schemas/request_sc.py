from marshmallow import fields
from app import ma

class RequestGetSchema(ma.Schema):
    request_id = fields.String(dump_only=True)
    user_id_self = fields.String()
    user_id_connection = fields.String()
    created_at = fields.DateTime(dump_only=True)
    is_accepted = fields.Boolean()

class RequestCreateSchema(ma.Schema):
    user_id_self = fields.String(required=True)
    user_id_connection = fields.String(required=True)

class RequestUpdateSchema(ma.Schema):
    is_accepted = fields.Boolean(required=True)
