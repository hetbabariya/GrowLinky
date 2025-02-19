from app import db
from app.models.post import Post
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

def create_post(user_id, data):

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")


    new_post = Post(
        user_id=user.user_id,
        post_caption=data.get("post_caption"),
        post_image=data.get("post_image"),
        like_count=data.get("like_count", 0), 
        comment_count=data.get("comment_count", 0), 
        is_deleted=data.get("is_deleted", False) 
    )

    try:
    
        db.session.add(new_post)
        db.session.commit()
        return new_post
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Post creation failed due to a database error")


def update_post(post_id, data):

    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")


    for key, value in data.items():
        if value is not None:
            setattr(post, key, value)

    try:
    
        db.session.commit()
        return post
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Post update failed due to a database error")


def delete_post(post_id):

    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")

    try:
    
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Post deletion failed due to a database error")


def get_post_by_id(post_id):

    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")

    return post


def get_all_posts(limit=10, offset=0):

    posts = Post.query.limit(limit).offset(offset).all()
    return posts
