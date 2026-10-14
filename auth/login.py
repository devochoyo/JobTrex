from flask import jsonify
from werkzeug.security import check_password_hash
from model.model import User
from flask_jwt_extended import create_access_token, create_refresh_token

def user_login(email, password):
    
    
    if not email:
        return jsonify({"msg": "Email cannot be empty"}), 400
    
    if not password:
        return jsonify({"msg": "Password cannot be empty"}), 400
    
    if '@' not in email:
        return jsonify({"msg": "Invalid email format"}), 400
    
    if len(password) < 6:
        return jsonify({"msg": "Password must be at least 6 characters long"}), 400
       
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({
            "msg": "Invalid email or password"
            }),401
    role = user.role.value
    psw = user.password
    
    pass_check = check_password_hash(psw, password)
    
    if not pass_check:
        return jsonify({
            "msg": "Invalid email or password"
            }),401
        
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        "msg": "Login successful",
         "role": role,
        "is_verified": bool(user.is_verified),
        "access_token": access_token,
        "refresh_token": refresh_token
    }),200

    
