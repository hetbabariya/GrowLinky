from marshmallow import fields
from app import ma
  


class LikeGetSchema(ma.Schema):  
    
    like_id = fields.String(dump_only=True)  
    post_id = fields.String(required=True)  
    user_id_like = fields.String(required=True)  
    created_at = fields.DateTime(dump_only=True)  
    updated_at = fields.DateTime(dump_only=True)  
    
    
    post = fields.Nested("PostGetSchema", dump_only=True)  

    
    user = fields.Nested("UserGetSchema", dump_only=True)  


class LikePostSchema(ma.Schema):
    post_id = fields.String(required=True)  
    user_id_like = fields.String(required=True)  
