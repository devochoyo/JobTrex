import email

from flask import jsonify
from werkzeug.security import check_password_hash
from model.model import User
from flask_jwt_extended import create_access_token, create_refresh_token

def user_login(email, password):
    
    
    if not email:
        return jsonify({"message": "Email cannot be empty"}), 400
    
    if not password:
        return jsonify({"message": "Password cannot be empty"}), 400
    
    if '@' not in email:
        return jsonify({"message": "Invalid email format"}), 400
    
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long"}), 400
       
    
    user = User.query.filter_by(email=email).first()
    role = user.role.value
    psw = user.password
    
    pass_check = check_password_hash(psw, password)
    
    if not user or not pass_check:
        return jsonify({
            "message": "Invalid email or password"
            }),401
        
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        "message": "Login successful",
         "role": role,
        "access_token": access_token,
        "refresh_token": refresh_token
    }),200

    
