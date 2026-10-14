from flask import jsonify
from model.model import OTP
from datetime import datetime, timedelta, timezone
from extension import db

def verify_otp(otp, email=None):
    
    if not otp:
        return jsonify({"msg": "OTP is required"}), 400
    
    otp = str(otp).strip()
    now = datetime.now(timezone.utc)
    
    entries = OTP.query.filter_by(otp=otp)
    if email:
        entries = entries.filter_by(email=str(email).strip())
    entries = entries.order_by(OTP.created_at.desc()).all()
    
    if not entries:
        return jsonify({"msg": "Invalid OTP"}), 400
    
    otp_entry = None
    for entry in entries:
        if not entry.used and now <= entry.expire_at:
            otp_entry = entry
            break
    
    if otp_entry is None:
        if all(entry.used for entry in entries):
            return jsonify({"msg": "OTP has been used"}), 400
        return jsonify({"msg": "OTP has expired"}), 400
        
    
    otp_entry.used = True
    # the user has 5 minutes after verifying to reset the password
    otp_entry.expire_at = now + timedelta(minutes=5)
    db.session.commit()
    
    return jsonify({"status": True, "msg": "OTP verified successfully"}), 200
