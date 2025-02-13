from app import db
from app.models.profile import Profile
from app.models.user import User

from sqlalchemy.exc import IntegrityError

# profile get by username
def get_profile_by_username(user_id):

    user = User.query.filter_by(user_id = user_id).first()
    if not user:
        raise ValueError("User not found")

    profile = Profile.query.filter_by(user_id=user.user_id).first()
    if not profile:
            raise ValueError("Profile not found")

    return profile



# create Profile
def create_profile(user_id ,data):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    existing_profile = Profile.query.filter_by(user_id=user.user_id).first()
    if existing_profile:
        raise ValueError("Profile already exists for this user")

    new_profile = Profile(
        user_id=user.user_id,
        profile_name=data["profile_name"],
        subheading=data.get("subheading"),
        skills=data.get("skills"),
        bio=data.get("bio"),
        gender=data["gender"],
        mobile_no=data.get("mobile_no"),
        social_links=data.get("social_links"),
        experience=data.get("experience"),
        dp_link=data.get("dp_link"),
        is_public=data.get("is_public", True)
    )

    try:
        db.session.add(new_profile)
        db.session.commit()
        return new_profile
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Profile creation failed due to a database error")



# profile update by username
def update_profile(user_id, data):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    profile = Profile.query.filter_by(user_id=user.user_id).first()
    if not profile:
        raise ValueError("Profile not found")

    for key, value in data.items():
        if value is not None:
            setattr(profile, key, value)

    try:
        db.session.commit()
        return profile
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Profile update failed due to a database error")



# delete profile
def delete_profile(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found")

    profile = Profile.query.filter_by(user_id=user.user_id).first()
    if not profile:
        raise ValueError("Profile not found")

    try:
        db.session.delete(profile)
        db.session.commit()
        return {"message": "Profile deleted successfully"}
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Profile deletion failed due to a database error")



# get all profiles
def get_all_profiles(limit=10, offset=0):
    profiles = Profile.query.limit(limit).offset(offset).all()
    return profiles
