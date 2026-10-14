from extension import db
from flask import jsonify
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from model.model import OTP,User

def reset_password(email, password, confirm_password):
    
    if not email:
         return jsonify({"msg": "email is required"}),400
    
    if not password:
         return jsonify({"msg": "password is required"}),400
     
    if not confirm_password:
         return jsonify({"msg": "confirm_password is required"}),400
    
    email = str(email).strip()
    password = str(password).strip()
    confirm_password = str(confirm_password).strip()
    
    if password != confirm_password:
        return jsonify({"msg": "password does not match"}),400
    
    if len(password) < 6:
        return jsonify({"msg": "Password must be at least 6 characters long"}),400
     
    otp_entry = (OTP.query.filter_by(email=email) .order_by(OTP.created_at.desc())
        .first()
            )
    otp_status = False
    if otp_entry is not None:

        otp_status = otp_entry.used and datetime.now(timezone.utc) <= otp_entry.expire_at
    if otp_status:
        hashed_pass = generate_password_hash(password=password)
        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({"msg": "User not found"}),400

        user.password = hashed_pass
        # the otp can only be used once to reset
        OTP.query.filter_by(email=email).delete()
        db.session.commit()
            
        return jsonify({
            "status": True,
            "msg": "Password Updated Successfully!"
        }),200
            
    return jsonify({
                "status": False,
                "msg": "Failed to update, please use the forgotten password first"
            }),400
