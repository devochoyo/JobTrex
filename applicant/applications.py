from flask import jsonify
from model.model import Application

def my_applications(applicant_id, page, per_page):
    
    applications = Application.query.filter_by(applicant_id=applicant_id).order_by(Application.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify([{
        "job_id": i.job.id,
        "title": i.job.title,
        "location": i.job.location,
        "salary": i.job.salary,
        "status": i.status.value
    }
    for i in applications.items
    ]), 200
