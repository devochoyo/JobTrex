from flask import request, jsonify
from model.model import Job

def all_jobs(page, per_page, search, location):
    
    url = request.host_url
    
    jobs = Job.query
    if search:
        jobs = jobs.filter(Job.title.ilike(f"%{search}%"))
    if location:
        jobs = jobs.filter(Job.location.ilike(f"%{location}%"))
    
    jobs = jobs.order_by(Job.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    res = []
    
    for job in jobs.items:
        jb = {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "salary": job.salary,
            "location": job.location,
            "picture": f"{url}{job.image}",
            "employer": job.employer.firstname + " " + job.employer.lastname
        }
        res.append(jb)
    return jsonify(res), 200
