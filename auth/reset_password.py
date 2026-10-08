from extension import db
from flask import jsonify
from werkzeug.security import generate_password_hash
from model.model import OTP,User

def reset_password(email, password, confirm_password):
    if password != confirm_password:
        return jsonify({"message": "password does not match"}),400
    
    if not email:
         return jsonify({"message": "email is required"}),400
    
    if not password:
         return jsonify({"message": "password is required"}),400
     
    if not confirm_password:
         return jsonify({"message": "confirm_password is required"}),400
     
    otp_entry = (OTP.query.filter_by(email=email) .order_by(OTP.created_at.desc())
        .first()
            )
    if otp_entry is not None:
        
        otp_status = otp_entry.used
    if otp_status:
        hashed_pass = generate_password_hash(password=password)
        user = User.query.filter_by(email=email)
            
        user.password = hashed_pass
        db.session.commit()
            
        return jsonify({
            "status": True,
            "message": "Password Updated Successfully!"
        }),200
            
    return jsonify({
                "status": False,
                "message": "Failed to update, please use the forgotten password first"
            }),400
   
    
    
    