from app import db
from app.models.comment import Comment
from app.models.user import User
from app.models.post import Post
from sqlalchemy.exc import IntegrityError

# Create Comment
def create_comment(user_id, data):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    post = Post.query.filter_by(post_id=data['post_id']).first()
    if not post:
        raise ValueError("Post not found")

    new_comment = Comment(
        post_id=data['post_id'],
        user_id=user.user_id,
        comment_text=data['comment_text']
    )

    try:
        db.session.add(new_comment)
        post.comment_count += 1  # Increment comment count
        db.session.commit()
        return new_comment
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while creating the comment")

# Update Comment
def update_comment(comment_id, data):
    comment = Comment.query.filter_by(comment_id=comment_id).first()
    if not comment:
        raise ValueError("Comment not found")

    for key, value in data.items():
        if value is not None:
            setattr(comment, key, value)

    try:
        db.session.commit()
        return comment
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while updating the comment")

# Delete Comment
def delete_comment(comment_id):
    comment = Comment.query.filter_by(comment_id=comment_id).first()
    if not comment:
        raise ValueError("Comment not found")

    post = Post.query.filter_by(post_id=comment.post_id).first()

    try:
        db.session.delete(comment)
        if post and post.comment_count > 0:
            post.comment_count -= 1  # Decrement comment count
        db.session.commit()
        return {"message": "Comment deleted successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while deleting the comment")

# Get Comment By Post
def get_comments_for_post(post_id, limit=10, offset=0):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        raise ValueError("Post not found")

    comments = Comment.query.filter_by(post_id=post_id).limit(limit).offset(offset).all()
    return comments

# Get Comment By User
def get_comments_by_user(user_id, limit=10, offset=0):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    comments = Comment.query.filter_by(user_id=user_id).limit(limit).offset(offset).all()
    return comments

# Get Comment By ID
def get_comment_by_id(comment_id):
    comment = Comment.query.filter_by(comment_id=comment_id).first()
    if not comment:
        raise ValueError("Comment not found")
    return comment
