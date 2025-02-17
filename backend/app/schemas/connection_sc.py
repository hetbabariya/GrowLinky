from marshmallow import fields, validate
from app import ma


class ConnectionGetSchema(ma.Schema):
    
    
    connection_id = fields.String(dump_only=True)  
    user_id_self = fields.String(required=True)  
    user_id_connection = fields.String(required=True)  
    request_id = fields.String()  
    created_at = fields.DateTime(dump_only=True)  
    updated_at = fields.DateTime(dump_only=True)  
    is_active = fields.Boolean()  
     


class ConnectionPostSchema(ma.Schema):
    user_id_self = fields.String(required=True)  
    user_id_connection = fields.String(required=True)  
    request_id = fields.String()  
    is_active = fields.Boolean(default=True)  

 
