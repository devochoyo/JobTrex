import secrets
from auth.mail import send_mail
from flask import jsonify
from model.model import OTP
from datetime import timedelta,datetime, timezone
from extension import db


def send_reset_email(email):
    
    if not email:
        return jsonify({"message", "email is required"}),400
    
    if "@" not in email:
        return jsonify({"message": "please enter a valid email"}),400
    
    
    otp = str(secrets.randbits(19))
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=5)
    
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
        "message": "if email exist, a verification email has been sent to the provided address"
    }),200