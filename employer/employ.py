from flask import jsonify
from model.model import Application, JobStatus
from extension import db

def employ(job_id, applicant_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}), 400
    
    if not applicant_id:
        return jsonify({"msg": "Applicant ID is required"}), 400
    
    if applicant_id is None:
        return jsonify({"msg": "Applicant ID cannot be empty"}), 400
    
    if job_id is None:
        return jsonify({"msg": "Job ID cannot be empty"}), 400
        
    
    job = Application.query.filter_by(job_id=job_id, applicant_id=applicant_id).first()
    if job is None:
        return jsonify({"msg": "No Applicant Yet"}),400
    
    job.status = JobStatus.ACCEPTED
    db.session.commit()
    return jsonify({"msg": "Successfully Employed"}), 200

