from flask import request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer
from auth.mail import send_mail
from model.model import User

def send_verification(user_id):
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "User not found"}),404
    
    if user.is_verified:
        return jsonify({"msg": "Email already verified"}),400
    
    serializer = URLSafeTimedSerializer(current_app.config['JWT_SECRET_KEY'], salt='verify-email')
    token = serializer.dumps(user.email)
    link = f"{request.host_url}api/v1/verify-email?token={token}"
    
    subject = "JOBTREX - VERIFY YOUR EMAIL"
    body = f"Click the link below to verify your email, this link will expire in 24 hours, if you did'nt request for this kindly ignore this message\n\n{link}"
    
    try:
        send_mail(subject, user.email, body)
    except Exception:
        return jsonify({"status": False, "msg": "Failed to send verification email, please try again later"}),500
    
    return jsonify({"status": True, "msg": "Verification email sent"}),200
