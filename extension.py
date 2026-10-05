from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_token(header,payload):
    from model.model import Revoke
    
    jti = payload["jti"]
    revoke = Revoke.query.filter_by(jti=jti).first()
    if revoke:
        return True
    return False
        