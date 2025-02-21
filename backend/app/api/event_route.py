from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.event_services import (
    get_event_by_id, create_event, update_event, delete_event, get_all_events, get_events_by_user
)
from app.schemas.event_sc import EventGetSchema, EventPostSchema

event_bp = Blueprint('event', __name__)

# Get all events
@event_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    events = get_all_events(limit, offset)
    return jsonify(EventGetSchema(many=True).dump(events)), 200

# Get event by ID
@event_bp.route('/events/<string:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    try:
        event = get_event_by_id(event_id)
        return jsonify(EventGetSchema().dump(event)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Get events for a user
@event_bp.route('/users/<string:user_id>/events', methods=['GET'])
@jwt_required()
def get_user_events(user_id):
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    try:
        events = get_events_by_user(user_id, limit, offset)
        return jsonify(EventGetSchema(many=True).dump(events)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Create an event
@event_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event_api():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        event = create_event(current_user_id, data)
        return jsonify(EventGetSchema().dump(event)), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

# Update an event
@event_bp.route('/events/<string:event_id>', methods=['PUT'])
@jwt_required()
def update_event_api(event_id):
    try:
        data = request.get_json()
        event = update_event(event_id, data)
        return jsonify(EventGetSchema().dump(event)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

# Delete an event
@event_bp.route('/events/<string:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event_api(event_id):
    try:
        message = delete_event(event_id)
        return jsonify(message), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
