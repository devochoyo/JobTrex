from extension import db
from model.model import Revoke

def revoke_token(jti):
    
    res = Revoke(jti=jti)
    db.session.add(res)
    db.session.commit()
    
    return True
