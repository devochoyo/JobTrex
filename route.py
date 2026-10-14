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
from applicant.apply import apply
from employer.applicants import applicants
from employer.employ import employ
from employer.employed import employed
from applicant.jobs import all_jobs
from applicant.job_details import job_details
from applicant.applications import my_applications
from applicant.withdraw import withdraw
from employer.reject import reject
from employer.edit_job import edit_job
from employer.delete_job import delete_job
from employer.applicant_profile import applicant_profile
from auth.profile import profile
from auth.update_profile import update_profile
from auth.change_password import change_password
from auth.send_verification import send_verification
from auth.verify_email import verify_email


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
apply_bp = Blueprint('apply', __name__)
applicant_bp = Blueprint('applicant', __name__)
employ_bp = Blueprint('employ', __name__)
employed_bp = Blueprint('employed', __name__)
jobs_bp = Blueprint('jobs', __name__)
job_details_bp = Blueprint('job_details', __name__)
my_applications_bp = Blueprint('my_applications', __name__)
withdraw_bp = Blueprint('withdraw', __name__)
reject_bp = Blueprint('reject', __name__)
edit_job_bp = Blueprint('edit_job', __name__)
delete_job_bp = Blueprint('delete_job', __name__)
applicant_profile_bp = Blueprint('applicant_profile', __name__)
profile_bp = Blueprint('profile', __name__)
update_profile_bp = Blueprint('update_profile', __name__)
change_password_bp = Blueprint('change_password', __name__)
send_verification_bp = Blueprint('send_verification', __name__)
verify_email_bp = Blueprint('verify_email', __name__)



@health_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"msg": "API is healthy"}), 200
    


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
        return jsonify({"msg": "Invalid role"}), 400
    
    if not role:
        return jsonify({"msg": "Role is required"}), 400
    
    if role not in ['applicant', 'employer']:
        return jsonify({"msg": "Invalid role"}), 400
    
    
    
@login_bp.route('/api/v1/login', methods=['POST'])
def login_route():
    
    data = request.get_json(silent=True) or {}
    email = data.get('email') or ''
    password = data.get('password') or ''
    
    u_email = str(email).strip()
    u_password = str(password).strip()
    
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
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    
    res = send_reset_email(email)
    return res
    
@verify_bp.route("/api/v1/verify", methods=["POST"])
def verify():
    data = request.get_json(silent=True) or {}
    otp = data.get('otp')
    email = data.get('email')
    
    res = verify_otp(otp, email)
    return res
    

@reset_bp.route("/api/v1/reset", methods=["POST"])
def reset():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get("confirm_password")
    
    res = reset_password(email,password,confirm_password)
    return res
    
    
    
@create_job_bp.route("/api/v1/post-job", methods=["POST"])
@jwt_required()
def post_job():
    employer_id = int(get_jwt_identity())
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


@apply_bp.route("/api/v1/apply", methods=["POST"])
@jwt_required()
def apply_job():
    
    data = request.get_json(silent=True) or {}
    
    job_id = data.get('job_id')
    applicant_id = int(get_jwt_identity())
    
    res = apply(job_id, applicant_id)
    return res
    

@applicant_bp.route("/api/v1/applicants", methods=["GET"])
@jwt_required()
def get_applicants():
    
    job_id = request.args.get('job_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    employer_id = int(get_jwt_identity())
    
    res = applicants(job_id, page, per_page, employer_id)
    return res

@employ_bp.route("/api/v1/employ", methods=["POST"])
@jwt_required()
def employ_user():
    
    data = request.get_json(silent=True) or {}
    
    job_id = data.get('job_id')
    applicant_id = data.get('applicant_id')
    employer_id = int(get_jwt_identity())
    
    res = employ(job_id, applicant_id, employer_id)
    return res

@employed_bp.route("/api/v1/employed", methods=["GET"])
@jwt_required()
def get_employed():
    job_id = request.args.get('job_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    employer_id = int(get_jwt_identity())
    
    res = employed(job_id, page, per_page, employer_id)
    return res


@jobs_bp.route("/api/v1/jobs", methods=["GET"])
@jwt_required()
def browse_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search')
    location = request.args.get('location')
    
    res = all_jobs(page, per_page, search, location)
    return res


@job_details_bp.route("/api/v1/job", methods=["GET"])
@jwt_required()
def get_job():
    job_id = request.args.get('job_id', type=int)
    
    res = job_details(job_id)
    return res


@my_applications_bp.route("/api/v1/my-applications", methods=["GET"])
@jwt_required()
def get_my_applications():
    applicant_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    res = my_applications(applicant_id, page, per_page)
    return res


@withdraw_bp.route("/api/v1/withdraw", methods=["DELETE"])
@jwt_required()
def withdraw_application():
    applicant_id = int(get_jwt_identity())
    job_id = request.args.get('job_id', type=int)
    
    res = withdraw(job_id, applicant_id)
    return res


@reject_bp.route("/api/v1/reject", methods=["POST"])
@jwt_required()
def reject_user():
    data = request.get_json(silent=True) or {}
    
    job_id = data.get('job_id')
    applicant_id = data.get('applicant_id')
    employer_id = int(get_jwt_identity())
    
    res = reject(job_id, applicant_id, employer_id)
    return res


@edit_job_bp.route("/api/v1/edit-job", methods=["POST"])
@jwt_required()
def update_job():
    employer_id = int(get_jwt_identity())
    job_id = request.form.get('job_id', type=int)
    title = request.form.get('title')
    description = request.form.get('description')
    location = request.form.get('location')
    salary = request.form.get('salary')
    picture = request.files.get('picture')
    
    res = edit_job(job_id, title, description, location, salary, picture, employer_id)
    return res


@delete_job_bp.route("/api/v1/delete-job", methods=["DELETE"])
@jwt_required()
def remove_job():
    employer_id = int(get_jwt_identity())
    job_id = request.args.get('job_id', type=int)
    
    res = delete_job(job_id, employer_id)
    return res


@applicant_profile_bp.route("/api/v1/applicant-profile", methods=["GET"])
@jwt_required()
def get_applicant_profile():
    employer_id = int(get_jwt_identity())
    job_id = request.args.get('job_id', type=int)
    applicant_id = request.args.get('applicant_id', type=int)
    
    res = applicant_profile(job_id, applicant_id, employer_id)
    return res


@profile_bp.route("/api/v1/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    
    res = profile(user_id)
    return res


@update_profile_bp.route("/api/v1/update-profile", methods=["POST"])
@jwt_required()
def edit_profile():
    user_id = int(get_jwt_identity())
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    country = request.form.get('country')
    profile_picture = request.files.get('profile_picture')
    cv = request.files.get('cv')
    
    res = update_profile(user_id, firstname, lastname, country, profile_picture, cv)
    return res


@change_password_bp.route("/api/v1/change-password", methods=["POST"])
@jwt_required()
def change_pass():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    res = change_password(user_id, old_password, new_password, confirm_password)
    return res


@send_verification_bp.route("/api/v1/send-verification", methods=["POST"])
@jwt_required()
def send_verify_email():
    user_id = int(get_jwt_identity())
    
    res = send_verification(user_id)
    return res


@verify_email_bp.route("/api/v1/verify-email", methods=["GET"])
def verify_user_email():
    token = request.args.get('token')
    
    res = verify_email(token)
    return res
