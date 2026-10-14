from flask import request, jsonify
from model.model import User

def user_data(user):
    
    url = request.host_url
    
    picture = None
    if user.profile_picture:
        picture = f"{url}{user.profile_picture}"
    
    cv = None
    if user.cv:
        cv = f"{url}{user.cv}"
    
    return {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "role": user.role.value,
        "country": user.country,
        "profile_picture": picture,
        "cv": cv,
        "is_verified": bool(user.is_verified)
    }


def profile(user_id):
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "User not found"}),404
    
    return jsonify(user_data(user)),200
