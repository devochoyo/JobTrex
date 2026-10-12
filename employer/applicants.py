from flask import jsonify
from model.model import Application

def applicants(job_id, page, per_page):
    
    job = Application.query.filter_by(job_id=job_id).paginate(page=page, per_page=per_page)
    if job is None:
        return jsonify({"msg": "No Applicant Yet"}),400
    return jsonify([{
        "job_id": i.job.id,
        "title": i.job.title,
        "applicants": i.applicant.firstname + " " + i.applicant.lastname,
        "status": i.status.value
    }
    for i in job
    ]), 200
    
    
    


    
    