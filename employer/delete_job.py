from flask import jsonify
from model.model import Application, Job
from extension import db

def delete_job(job_id, employer_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}),400
    
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return jsonify({"msg": "Job not found"}),404
    
    if job.employer_id != employer_id:
        return jsonify({"msg": "You can only delete your own jobs"}),403
    
    Application.query.filter_by(job_id=job_id).delete()
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({"status": True, "msg": "Job Deleted Successfully!"}),200
