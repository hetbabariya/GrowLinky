from io import BytesIO
from flask import jsonify
from app import db
from app.models.post import Post
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
import base64
import os
import uuid
from PIL import Image
from sqlalchemy.orm import joinedload


# Update Post
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



# Delete Post
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



# Get Post by Id
def get_post_by_id(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")

    return post



# Get All Post By User
def get_all_posts_by_user(user_id):
    """Fetch all posts of a specific user"""
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    posts = Post.query.filter_by(user_id=user_id, is_deleted=False).order_by(Post.created_at.desc()).all()

    if not posts:
        raise ValueError("No posts found for this user")

    return posts



# Get All Post
# def get_all_posts(limit=10, offset=0):
#     posts = Post.query.limit(limit).offset(offset).all()
#     return posts


def get_all_posts(limit=10, offset=0):
    posts = (
        Post.query
        .options(joinedload(Post.user))  # Preload user relationship
        .filter_by(is_deleted=False)  # Exclude deleted posts
        .order_by(Post.created_at.desc())  # Order by latest posts
        .limit(limit)
        .offset(offset)
        .all()
    )

    post_list = [
        {
            "post_id": post.post_id,
            "post_caption": post.post_caption,
            "post_image": post.post_image,
            "like_count": post.like_count,
            "comment_count": post.comment_count,
            "created_at": post.created_at,
            "user_name": post.user.user_name  # Assuming `user_name` exists in User model
        }
        for post in posts
    ]

    return post_list


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_base64_image(image_data):
    """Save base64 image data to file system"""
    if not image_data:
        return None

    try:
        # Split the base64 string in case it contains the data URL prefix
        if ',' in image_data:
            header, image_data = image_data.split(',', 1)

        # Decode base64 string
        image_bytes = base64.b64decode(image_data)

        # Verify it's a valid image
        img = Image.open(BytesIO(image_bytes))

        # Generate unique filename
        file_name = f"{uuid.uuid4()}.{img.format.lower()}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Save image
        img.save(file_path, format=img.format)

        return file_path

    except Exception as e:
        raise ValueError(f"Image processing error: {str(e)}")

def create_post(user_id,data):

    print(data)
    print("---------------------------------")
    if not data.get('post_caption') and not data.get('post_image'):
        return jsonify({"error": "Post must contain either text or image"}), 400

    # Process image if provided
    image_path = None
    if data.get('post_image'):
        try:
            image_path = save_base64_image(data['post_image'])
        except ValueError as e:
            return jsonify({"error": f"Image processing failed: {str(e)}"}), 400

    # Create post
    try:

        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            raise ValueError("User not found")

        # Create new post
        new_post = Post(
            user_id=user_id,
            post_caption=data.get("post_caption", ""),
            post_image=image_path,
            like_count=0,
            comment_count=0,
            is_deleted=False
        )

        try:
            db.session.add(new_post)
            db.session.commit()
            return new_post
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Post creation failed due to a database error")

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
