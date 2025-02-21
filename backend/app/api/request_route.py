from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.request_services import (
    create_request,
    get_send_requests_for_user,
    update_request,
    delete_request,
    get_requests_for_user,
    get_request_by_id,
)
from app.schemas.request_sc import RequestCreateSchema, RequestUpdateSchema, RequestGetSchema

request_bp = Blueprint("request_bp", __name__)

# Create a new request
@request_bp.route("/requests", methods=["POST"])
@jwt_required()
def create_new_request():
    try:
        schema = RequestCreateSchema()
        data = schema.load(request.get_json())
        current_user = get_jwt_identity()

        if current_user != data["user_id_self"]:
            return jsonify({"error": "Unauthorized"}), 403

        request_obj = create_request(data)
        return jsonify(RequestGetSchema().dump(request_obj)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


# Accept or reject a request
@request_bp.route("/requests/<string:request_id>", methods=["PUT"])
@jwt_required()
def update_existing_request(request_id):
    try:
        schema = RequestUpdateSchema()
        data = schema.load(request.get_json())

        request_obj = update_request(request_id, data["is_accepted"])
        return jsonify(RequestGetSchema().dump(request_obj)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Delete a request
@request_bp.route("/requests/<string:request_id>", methods=["DELETE"])
@jwt_required()
def delete_existing_request(request_id):
    try:
        response = delete_request(request_id)
        return jsonify(response), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Get all requests for a user
@request_bp.route("/requests", methods=["GET"])
@jwt_required()
def get_all_requests_for_user():
    try:
        user_id = get_jwt_identity()
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)

        requests = get_requests_for_user(user_id, limit, offset)
        return jsonify(RequestGetSchema(many=True).dump(requests)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


# Get request by ID
@request_bp.route("/requests/<string:request_id>", methods=["GET"])
@jwt_required()
def get_request_details(request_id):
    try:
        request_obj = get_request_by_id(request_id)
        return jsonify(RequestGetSchema().dump(request_obj)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Get Send Connection Requests
@request_bp.route("/send/requests", methods=["GET"])
@jwt_required()
def get_all_send_requests_for_user():
    try:
        user_id = get_jwt_identity()
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)

        requests = get_send_requests_for_user(user_id, limit, offset)
        return jsonify(RequestGetSchema(many=True).dump(requests)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404