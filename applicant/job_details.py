from flask import request, jsonify
from model.model import Job

def job_details(job_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}),400
    
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return jsonify({"msg": "Job not found"}),404
    
    url = request.host_url
    
    return jsonify({
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "salary": job.salary,
        "location": job.location,
        "picture": f"{url}{job.image}",
        "employer": job.employer.firstname + " " + job.employer.lastname
    }),200
