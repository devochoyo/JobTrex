from flask import Blueprint, request, jsonify
from auth.register import applicant_reg,employer_reg
#from auth.login import login
#from auth.logout import logout
#from auth.refresh import refresh
#from auth.verify import verify


register_bp = Blueprint('register', __name__)
login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)
refresh_bp = Blueprint('refresh', __name__)

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
    
    
    
    
    
