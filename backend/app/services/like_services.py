from app import db
from app.models.like import Like
from app.models.post import Post
from app.models.user import User
from sqlalchemy.exc import IntegrityError

def create_like(user_id, post_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")

    existing_like = Like.query.filter_by(user_id_like=user_id, post_id=post_id).first()
    if existing_like:
        raise ValueError("User has already liked this post")

    new_like = Like(
        user_id_like=user.user_id,
        post_id=post.post_id
    )

    try:
        db.session.add(new_like)
        post.like_count += 1  # Increment like count
        db.session.commit()
        return new_like
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while creating the like")

def delete_like(user_id, post_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")

    like = Like.query.filter_by(user_id_like=user_id, post_id=post_id).first()
    if not like:
        raise ValueError("Like not found")

    try:
        db.session.delete(like)
        post.like_count = max(0, post.like_count - 1)  # Decrement like count, ensure it doesn't go negative
        db.session.commit()
        return {"message": "Like deleted successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while deleting the like")

def get_likes_for_post(post_id, limit=10, offset=0):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")

    likes = Like.query.filter_by(post_id=post_id).limit(limit).offset(offset).all()
    return likes

def get_like_by_id(like_id):
    like = Like.query.filter_by(like_id=like_id).first()
    if not like:
        raise ValueError("Like not found")
    return like
