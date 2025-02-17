from marshmallow import fields, validate
from app import ma



class EventGetSchema(ma.Schema):
    
    event_id = fields.String(dump_only=True)  
    user_fid = fields.String(required=True)  
    event = fields.String(required=True)  
    comment = fields.String()  
    created_at = fields.DateTime(dump_only=True)  
    updated_at = fields.DateTime(dump_only=True)  
    is_active = fields.Boolean()  
     

class EventPostSchema(ma.Schema):
    user_fid = fields.String(required=True)  
    event = fields.String(required=True)  
    comment = fields.String()  
    is_active = fields.Boolean(default=True)  
