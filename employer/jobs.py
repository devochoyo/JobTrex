from flask import request,jsonify
from model.model import Job

def employer_jobs(employer_id):
    
    url = request.host_url
    
    jobs = Job.query.filter_by(employer_id=employer_id).all()
    if jobs is None:
        return jsonify({"status": False, "msg": "No job created yet"}),400
    
    res = []
    
    for job in jobs:
        jb = {
            "title": job.title,
            "description": job.description,
            "salary": job.salary,
            "location": job.location,
            "picture": f"{url}{job.image}"
        }
        res.append(jb)
    return jsonify(res)


    
        