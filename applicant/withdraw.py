from flask import jsonify
from model.model import Application
from extension import db

def withdraw(job_id, applicant_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}),400
    
    application = Application.query.filter_by(job_id=job_id, applicant_id=applicant_id).first()
    if application is None:
        return jsonify({"msg": "Application not found"}),404
    
    db.session.delete(application)
    db.session.commit()
    
    return jsonify({"status": True, "msg": "Application withdrawn successfully"}),200
