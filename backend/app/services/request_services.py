from app import db
from app.models.request import Request
from app.models.user import User
from sqlalchemy.exc import IntegrityError

# Create a new request
def create_request(data):
    user_self = User.query.get(data["user_id_self"])
    user_connection = User.query.get(data["user_id_connection"])

    if not user_self or not user_connection:
        raise ValueError("User not found")

    # Prevent duplicate requests
    existing_request = Request.query.filter_by(
        user_id_self=data["user_id_self"], user_id_connection=data["user_id_connection"]
    ).first()

    if existing_request:
        raise ValueError("Request already exists")

    new_request = Request(**data)

    try:
        db.session.add(new_request)
        db.session.commit()
        return new_request
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while creating the request")


# Accept or reject a request
def update_request(request_id, is_accepted):
    request = Request.query.get(request_id)

    if not request:
        raise ValueError("Request not found")

    request.is_accepted = is_accepted

    try:
        db.session.commit()
        return request
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while updating the request")


# Delete a request
def delete_request(request_id):
    request = Request.query.get(request_id)

    if not request:
        raise ValueError("Request not found")

    try:
        db.session.delete(request)
        db.session.commit()
        return {"message": "Request deleted successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while deleting the request")


# Get all requests for a user
def get_requests_for_user(user_id, limit=10, offset=0):
    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found")

    return Request.query.filter_by(user_id_connection=user_id).limit(limit).offset(offset).all()


# Get request details by ID
def get_request_by_id(request_id):
    request = Request.query.get(request_id)

    if not request:
        raise ValueError("Request not found")

    return request
