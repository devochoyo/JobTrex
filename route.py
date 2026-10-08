from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from auth.register import applicant_reg,employer_reg
from auth.login import user_login
from auth.refresh import refresh_token
from auth.send_otp import send_reset_email 
from auth.logout import user_logout
from auth.verify_otp import verify_otp
from auth.reset_password import reset_password
from employer.create_job import create_job
from employer.jobs import employer_jobs


register_bp = Blueprint('register', __name__)
login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)
refresh_bp = Blueprint('refresh', __name__)
health_bp = Blueprint('health', __name__)
forgotten_password_bp = Blueprint('forgotten_password',__name__)
verify_bp = Blueprint('verify',__name__)
reset_bp = Blueprint('reset', __name__)
create_job_bp = Blueprint('create', __name__)
employer_jobs_bp = Blueprint('employer_jobs', __name__)



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
    
    

@forgotten_password_bp.route("/api/v1/forgot-password", methods=["POST"])
def forgot_pass():
    email = request.get_json().get('email')
    
    if not None:
        res = send_reset_email(email)
        return res
    
@verify_bp.route("/api/v1/verify", methods=["POST"])
def verify():
    otp = request.get_json().get('otp')
    
    if not None:
        res = verify_otp(otp)
        return res
    

@reset_bp.route("/api/v1/reset", methods=["POST"])
def verify():
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    confirm_password = request.get_json().get("confirm_password")
    
    res = reset_password(email,password,confirm_password)
    return res
    
    
    
@create_job_bp.route("/api/v1/post-job", methods=["POST"])
@jwt_required()
def post_job():
    employer_id = get_jwt_identity()
    title = request.form.get('title')
    description = request.form.get('description')
    location = request.form.get('location')
    salary = request.form.get('salary')
    picture = request.files.get('picture')
    
    res = create_job(title, description, location, salary, picture, employer_id)
    
    return res


@employer_jobs_bp.route("/api/v1/my-jobs", methods=["GET"])
@jwt_required()
def emp_jobs():
    employer_id = int(get_jwt_identity())
    
    res = employer_jobs(employer_id)
    return res
