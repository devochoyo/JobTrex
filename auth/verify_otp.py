from flask import jsonify
from model.model import OTP
from datetime import datetime, timezone
from extension import db

def verify_otp(otp):
    
    if not otp:
        return jsonify({"message": "OTP is required"}), 400
    
    otp_entry = OTP.query.filter_by(otp=otp).first()
    
    if not otp_entry:
        return jsonify({"message": "Invalid OTP"}), 400
    
    if datetime.now(timezone.utc) > otp_entry.expire_at:
        return jsonify({"message": "OTP has expired"}), 400
    
    if  otp_entry.used:
        return jsonify({"message": "OTP has beed used"}), 400
        
    
    otp_entry.used = True
    db.session.commit()
    
    return jsonify({"status": True, "message": "OTP verified successfully"}), 200