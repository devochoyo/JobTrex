from extension import db
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from model.model import User

def change_password(user_id, old_password, new_password, confirm_password):
    
    if not old_password:
        return jsonify({"msg": "old_password is required"}),400
    
    if not new_password:
        return jsonify({"msg": "new_password is required"}),400
    
    if not confirm_password:
        return jsonify({"msg": "confirm_password is required"}),400
    
    old_password = str(old_password).strip()
    new_password = str(new_password).strip()
    confirm_password = str(confirm_password).strip()
    
    if new_password != confirm_password:
        return jsonify({"msg": "password does not match"}),400
    
    if len(new_password) < 6:
        return jsonify({"msg": "Password must be at least 6 characters long"}),400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "User not found"}),404
    
    if not check_password_hash(user.password, old_password):
        return jsonify({"msg": "Old password is incorrect"}),400
    
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({"status": True, "msg": "Password changed successfully!"}),200
