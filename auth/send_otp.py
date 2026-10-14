import secrets
from auth.mail import send_mail
from flask import jsonify
from model.model import OTP, User
from datetime import timedelta,datetime, timezone
from extension import db


def send_reset_email(email):
    
    if not email:
        return jsonify({"msg": "email is required"}),400
    
    email = str(email).strip()
    
    if "@" not in email:
        return jsonify({"msg": "please enter a valid email"}),400
    
    # remove expired otps
    OTP.query.filter(OTP.expire_at < datetime.now(timezone.utc)).delete()
    db.session.commit()
    
    user = User.query.filter_by(email=email).first()
    
    if user is not None:
        otp = str(secrets.randbelow(1000000)).zfill(6)
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        # only the latest otp of an email is valid
        OTP.query.filter_by(email=email).delete()
        
        res = OTP(
                otp = otp,
                email = email,
                expire_at = expire_time
                )

        db.session.add(res)
        db.session.commit()
        
        
        reciever = email
        subject = "JOBTREX - OTP VERIFICATION"
        body = f"Your verification code is {otp}, this code will expire in 5 minutes, if you did'nt request for this kindly ignore this message"
        
        send_mail(subject, reciever, body)
    
    
    return jsonify({
        "status": True,
        "msg": "if email exist, a verification email has been sent to the provided address"
    }),200
