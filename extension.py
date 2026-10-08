from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
@jwt.token_in_blocklist_loader
def check_token(header,payload):
    from model.model import Revoke
    
    jti = payload["jti"]
    revoke = Revoke.query.filter_by(jti=jti).first()
    if revoke:
        return True
    return False
        