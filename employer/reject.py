from flask import jsonify
from model.model import Application, Job, JobStatus
from extension import db
from auth.mail import send_mail

def reject(job_id, applicant_id, employer_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}), 400
    
    if not applicant_id:
        return jsonify({"msg": "Applicant ID is required"}), 400
    
    try:
        job_id = int(job_id)
        applicant_id = int(applicant_id)
    except (TypeError, ValueError):
        return jsonify({"msg": "Job ID and Applicant ID must be numbers"}), 400
    
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return jsonify({"msg": "Job not found"}), 404
    
    if job.employer_id != employer_id:
        return jsonify({"msg": "You can only reject applicants of your own jobs"}), 403
    
    application = Application.query.filter_by(job_id=job_id, applicant_id=applicant_id).first()
    if application is None:
        return jsonify({"msg": "No Applicant Yet"}),400
    
    application.status = JobStatus.REJECTED
    db.session.commit()
    
    try:
        send_mail("JOBTREX - APPLICATION UPDATE", application.applicant.email, f"Sorry, your application for the job: {job.title} was not successful")
    except Exception:
        pass
    
    return jsonify({"msg": "Successfully Rejected"}), 200
