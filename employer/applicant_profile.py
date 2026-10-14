from flask import jsonify
from model.model import Application, Job
from auth.profile import user_data

def applicant_profile(job_id, applicant_id, employer_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}),400
    
    if not applicant_id:
        return jsonify({"msg": "Applicant ID is required"}),400
    
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return jsonify({"msg": "Job not found"}),404
    
    if job.employer_id != employer_id:
        return jsonify({"msg": "You can only view applicants of your own jobs"}),403
    
    application = Application.query.filter_by(job_id=job_id, applicant_id=applicant_id).first()
    if application is None:
        return jsonify({"msg": "This user did not apply for your job"}),404
    
    return jsonify(user_data(application.applicant)),200
