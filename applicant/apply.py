from flask import jsonify
from model.model import Application
from extension import db

def apply(job_id, applicant_id):
    
    if not applicant_id:
        return jsonify({"msg": "Applicant id is required"}),400
    
    if not job_id:
        return jsonify({"msg": "Job id is required"}),400
    
    try:
        apply = Application(job_id=job_id, applicant_id=applicant_id)
        db.session.add(apply)
        db.session.commit()
        
        return jsonify({
            "status": True,
            "msg": "Application submitted successfully!"
        }),200
    except:
        db.session.rollback()
        return jsonify({
            "status": False,
            "msg": "Failed to apply, please try again later"
        }),500