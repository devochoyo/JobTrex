from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from auth.register import applicant_reg,employer_reg
from auth.login import user_login
from auth.refresh import refresh_token
#from auth.login import login
from auth.logout import user_logout
#from auth.refresh import refresh
#from auth.verify import verify


register_bp = Blueprint('register', __name__)
login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)
refresh_bp = Blueprint('refresh', __name__)
health_bp = Blueprint('health', __name__)



@health_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"message": "API is healthy"}), 200



@register_bp.route('/api/v1/register', methods=['POST'])
def register():
    
    firstname  = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    country = request.form.get('country')
    profile_picture = request.files.get('profile_picture')
    cv = request.files.get('cv')
    
    
    if role == 'applicant':
        
        res = applicant_reg(firstname, lastname, email, password, role, country, profile_picture, cv)
        return res

    if role == 'employer':
        res = employer_reg(firstname, lastname, email, password, role, country, profile_picture)
        return res
    
    if role == 'admin':
        return jsonify({"message": "Invalid role"}), 400
    
    if not role:
        return jsonify({"message": "Role is required"}), 400
    
    if role not in ['applicant', 'employer']:
        return jsonify({"message": "Invalid role"}), 400
    
    
    
@login_bp.route('/api/v1/login', methods=['POST'])
def login_route():
    
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    
    u_email = email.strip()
    u_password = password.strip()
    
    res = user_login(u_email, u_password)
    return res


@logout_bp.route("/api/v1/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    payload = get_jwt()
    
    jti = payload["jti"]
    res = user_logout(jti)
    return res


@refresh_bp.route("/api/v1/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    
    user_id = get_jwt_identity()
    
    res = refresh_token(user_id)
    return res
    
    
    
