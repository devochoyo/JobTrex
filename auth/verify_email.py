from flask import jsonify, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from model.model import User
from extension import db

def verify_email(token):
    
    if not token:
        return jsonify({"msg": "Token is required"}),400
    
    serializer = URLSafeTimedSerializer(current_app.config['JWT_SECRET_KEY'], salt='verify-email')
    
    try:
        email = serializer.loads(token, max_age=86400)
    except SignatureExpired:
        return jsonify({"msg": "Verification link has expired"}),400
    except BadSignature:
        return jsonify({"msg": "Invalid verification link"}),400
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "User not found"}),404
    
    user.is_verified = True
    db.session.commit()
    
    return jsonify({"status": True, "msg": "Email verified successfully"}),200
