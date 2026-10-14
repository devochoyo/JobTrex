from flask_mail import Message
from extension import mail
from model.model import User
def send_mail(subject, reciever, body):
    user = User.query.filter_by(email=reciever).first()
    
    if user is None:
        return False
    
    msg = Message(
        subject = subject,
        recipients=[reciever],
        body=body
    )
    
    mail.send(msg)
    return True
