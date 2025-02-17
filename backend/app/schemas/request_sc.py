from marshmallow import fields
from app import ma  

class RequestGetSchema(ma.Schema):
    
    request_id = fields.String(dump_only=True)  
    post_id_self = fields.String(required=True)  
    user_id_connection = fields.String(required=True)  
    comment = fields.String()  
    created_at = fields.DateTime(dump_only=True)  
    is_accepted = fields.Boolean()  

    
    user = fields.Nested("UserGetSchema", dump_only=True)  
    
    
    post = fields.Nested("PostGetSchema", dump_only=True)  

class RequestPostSchema(ma.Schema):
    post_id_self = fields.String(required=True)  
    user_id_connection = fields.String(required=True)  
    comment = fields.String()  
    is_accepted = fields.Boolean()  
