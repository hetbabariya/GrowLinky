from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.connection_services import (
    create_connection,
    delete_connection,
    get_connections_for_user,
    get_connection_by_id,
    update_connection,
)
from app.schemas.connection_sc import ConnectionPostSchema, ConnectionGetSchema, ConnectionUpdateSchema

connection_bp = Blueprint("connection_bp", __name__)

# Create a new connection
@connection_bp.route("/connections", methods=["POST"])
@jwt_required()
def create_new_connection():
    try:
        schema = ConnectionPostSchema()
        data = schema.load(request.get_json())

        # Ensure authenticated user is part of the connection
        if get_jwt_identity() not in [data["user_id_self"], data["user_id_connection"]]:
            return jsonify({"error": "Unauthorized"}), 403

        connection_obj = create_connection(data)
        return jsonify(ConnectionGetSchema().dump(connection_obj)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


# Update a connection
@connection_bp.route("/connections/<string:connection_id>", methods=["PUT"])
@jwt_required()
def update_existing_connection(connection_id):
    try:
        schema = ConnectionUpdateSchema(partial=True)
        data = schema.load(request.get_json())

        connection_obj = update_connection(connection_id, data)
        return jsonify(ConnectionGetSchema().dump(connection_obj)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Delete a connection
@connection_bp.route("/connections/<string:connection_id>", methods=["DELETE"])
@jwt_required()
def delete_existing_connection(connection_id):
    try:
        response = delete_connection(connection_id)
        return jsonify(response), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Get all connections for a user
@connection_bp.route("/connections", methods=["GET"])
@jwt_required()
def get_all_connections_for_user():
    try:
        user_id = get_jwt_identity()
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)

        connections = get_connections_for_user(user_id, limit, offset)
        return jsonify(ConnectionGetSchema(many=True).dump(connections)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Get connection by ID
@connection_bp.route("/connections/<string:connection_id>", methods=["GET"])
@jwt_required()
def get_connection_details(connection_id):
    try:
        connection_obj = get_connection_by_id(connection_id)
        return jsonify(ConnectionGetSchema().dump(connection_obj)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
