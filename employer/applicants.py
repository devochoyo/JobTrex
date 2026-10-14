from flask import jsonify
from model.model import Application, Job

def applicants(job_id, page, per_page, employer_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}),400
    
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return jsonify({"msg": "Job not found"}),404
    
    if job.employer_id != employer_id:
        return jsonify({"msg": "You can only view applicants of your own jobs"}),403
    
    applications = Application.query.filter_by(job_id=job_id).order_by(Application.id).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify([{
        "job_id": i.job.id,
        "title": i.job.title,
        "applicant_id": i.applicant.id,
        "applicants": i.applicant.firstname + " " + i.applicant.lastname,
        "status": i.status.value
    }
    for i in applications.items
    ]), 200
