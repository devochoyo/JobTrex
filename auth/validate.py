from model.model import User

def validate(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return True
    else:
        return False