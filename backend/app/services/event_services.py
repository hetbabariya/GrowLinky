from app import db
from app.models.events import Event
from app.models.user import User
from sqlalchemy.exc import IntegrityError

def get_event_by_id(event_id):
    event = Event.query.filter_by(event_id=event_id).first()
    if not event:
        raise ValueError("Event not found")
    return event

def create_event(user_id, data):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    new_event = Event(
        user_fid=user.user_id,
        event=data['event'],
        comment=data.get('comment', ""),
        is_active=data.get('is_active', True)
    )

    try:
        db.session.add(new_event)
        db.session.commit()
        return new_event
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while creating the event")

def update_event(event_id, data):
    event = Event.query.filter_by(event_id=event_id).first()
    if not event:
        raise ValueError("Event not found")

    for key, value in data.items():
        if value is not None:
            setattr(event, key, value)

    try:
        db.session.commit()
        return event
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while updating the event")

def delete_event(event_id):
    event = Event.query.filter_by(event_id=event_id).first()
    if not event:
        raise ValueError("Event not found")

    try:
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error occurred while deleting the event")

def get_all_events(limit=10, offset=0):
    events = Event.query.limit(limit).offset(offset).all()
    return events

def get_events_by_user(user_id, limit=10, offset=0):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    events = Event.query.filter_by(user_fid=user_id).limit(limit).offset(offset).all()
    return events
