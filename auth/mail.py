from flask_mail import Message
from extension import mail
from model.model import User
def send_mail(subject, reciever, body):
    user = User.query.filter_by(email=reciever).first()
    user_email = user.email
    
    
    msg = Message(
        subject = subject,
        recipients=[reciever],
        body=body
    )
    
    if user_email:
        mail.send(msg)
        return True
    
    return True