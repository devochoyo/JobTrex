from flask import jsonify
from model.model import Job
from extension import db
from uploads import job_photo

def edit_job(job_id, title, description, location, salary, photo, employer_id):
    
    if not job_id:
        return jsonify({"msg": "Job ID is required"}),400
    
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return jsonify({"msg": "Job not found"}),404
    
    if job.employer_id != employer_id:
        return jsonify({"msg": "You can only edit your own jobs"}),403
    
    if salary:
        try:
            salary = float(salary)
        except ValueError:
            return jsonify({"msg": "salary must be a number"}),400
    
    if photo:
        job_image = job_photo(photo)
        if job_image["status"] == False:
            return jsonify({"msg": job_image["msg"]}),400
        job.image = job_image["photo"]
    
    if title:
        job.title = title
    if description:
        job.description = description
    if location:
        job.location = location
    if salary:
        job.salary = salary
    
    db.session.commit()
    return jsonify({"status": True, "msg": "Job Updated Successfully!"}),200
