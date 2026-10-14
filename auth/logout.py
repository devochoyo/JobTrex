from auth.revoke_token import revoke_token
from flask import jsonify
def user_logout(jti):
    
    res = revoke_token(jti)
    
    if res:
        return jsonify({
            "status":True,
            "msg": "Logout Successful!"
        }),200
        
    return jsonify({
        'status': False,
        "msg": "Something went wrong"
    }),500