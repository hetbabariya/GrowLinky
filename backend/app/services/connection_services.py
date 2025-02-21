from app import db
from app.models.connection import Connection
from app.models.request import Request
from app.models.user import User
from sqlalchemy.exc import IntegrityError

# Create a new connection
def create_connection(data):
    user_self = User.query.get(data["user_id_self"])
    user_connection = User.query.get(data["user_id_connection"])

    if not user_self or not user_connection:
        raise ValueError("User not found")

    # Prevent duplicate connections
    existing_connection = Connection.query.filter_by(
        user_id_self=data["user_id_self"], user_id_connection=data["user_id_connection"]
    ).first()

    if existing_connection:
        raise ValueError("Connection already exists")

    # Ensure request exists and is accepted before creating connection
    request = Request.query.filter_by(
        user_id_self=data["user_id_connection"],
        user_id_connection=data["user_id_self"],
        is_accepted=True
    ).first()

    if not request:
        raise ValueError("No valid request found for connection")

    new_connection = Connection(**data)

    try:
        db.session.add(new_connection)
        db.session.commit()
        return new_connection
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while creating the connection")


# Update connection details (e.g., is_active status)
def update_connection(connection_id, data):
    connection = Connection.query.get(connection_id)

    if not connection:
        raise ValueError("Connection not found")

    for key, value in data.items():
        if value is not None:
            setattr(connection, key, value)

    try:
        db.session.commit()
        return connection
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while updating the connection")

# Remove a connection
def delete_connection(connection_id):
    connection = Connection.query.get(connection_id)

    if not connection:
        raise ValueError("Connection not found")

    try:
        db.session.delete(connection)
        db.session.commit()
        return {"message": "Connection deleted successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while deleting the connection")


# Get all connections for a user
def get_connections_for_user(user_id, limit=10, offset=0):
    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found")

    return Connection.query.filter(
        (Connection.user_id_self == user_id) | (Connection.user_id_connection == user_id)
    ).limit(limit).offset(offset).all()


# Get connection details by ID
def get_connection_by_id(connection_id):
    connection = Connection.query.get(connection_id)

    if not connection:
        raise ValueError("Connection not found")

    return connection
