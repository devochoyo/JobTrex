from flask import jsonify
from model.model import Application, Job, User, UserRole
from extension import db
from auth.mail import send_mail

def apply(job_id, applicant_id):
    
    if not applicant_id:
        return jsonify({"msg": "Applicant id is required"}),400
    
    if not job_id:
        return jsonify({"msg": "Job id is required"}),400
    
    user = User.query.filter_by(id=applicant_id).first()
    if user is None or user.role != UserRole.APPLICANT:
        return jsonify({"msg": "Only applicants can apply for jobs"}),403
    
    try:
        job_id = int(job_id)
    except (TypeError, ValueError):
        return jsonify({"msg": "Job id must be a number"}),400
    
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return jsonify({"msg": "Job not found"}),404
    
    already_applied = Application.query.filter_by(job_id=job_id, applicant_id=applicant_id).first()
    if already_applied:
        return jsonify({"msg": "You have already applied for this job"}),409
    
    try:
        apply = Application(job_id=job_id, applicant_id=applicant_id)
        db.session.add(apply)
        db.session.commit()
        
        try:
            send_mail("JOBTREX - NEW APPLICATION", job.employer.email, f"{user.firstname} {user.lastname} applied for your job: {job.title}")
        except Exception:
            pass
        
        return jsonify({
            "status": True,
            "msg": "Application submitted successfully!"
        }),200
    except Exception:
        db.session.rollback()
        return jsonify({
            "status": False,
            "msg": "Failed to apply, please try again later"
        }),500
