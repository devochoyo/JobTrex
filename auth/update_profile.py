from flask import jsonify
from model.model import User, UserRole
from extension import db
from uploads import file_uploads

def update_profile(user_id, firstname, lastname, country, profile_picture, cv):
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "User not found"}),404
    
    if cv and user.role != UserRole.APPLICANT:
        return jsonify({"msg": "Only applicants can upload a CV"}),400
    
    res = file_uploads(profile_picture, cv)
    if res['status'] == False:
        return jsonify({"msg": res['msg']}),400
    
    if res['profile_picture']:
        user.profile_picture = res['profile_picture']
    if 'cv' in res:
        user.cv = res['cv']
    
    if firstname and firstname.strip():
        user.firstname = firstname.strip()
    if lastname and lastname.strip():
        user.lastname = lastname.strip()
    if country and country.strip():
        user.country = country.strip()
    
    db.session.commit()
    return jsonify({"status": True, "msg": "Profile updated successfully!"}),200
