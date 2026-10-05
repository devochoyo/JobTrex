from flask import jsonify
from model.model import User
from flask_jwt_extended import create_access_token

def refresh_token(user_id):
    
    user = User.query.get(user_id)
    if user is not None:
        access_token = create_access_token(identity= str(user.id))
        
        return jsonify({
            "access_token": access_token
        }),200
        
    return jsonify({"message": "something went wrong"}),500
    
    