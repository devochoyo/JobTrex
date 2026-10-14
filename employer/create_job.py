from model.model import Job, User, UserRole
from flask import jsonify
from extension import db
from uploads import job_photo

def create_job(title, description, location, salary, photo, employer_id):
    
    user = User.query.filter_by(id=employer_id).first()
    if user is None or user.role != UserRole.EMPLOYER:
        return jsonify({"msg": "Only employers can post jobs"}),403
    
    if not title:
        return jsonify({"msg": "title is required"}),400
    
    if not description:
        return jsonify({"msg": "description is required"}),400
    
    if not location:
        return jsonify({"msg": "location is required"}),400
    
    if not salary:
        return jsonify({"msg": "salary is required"}),400

    if not photo:
        return jsonify({"msg": "job photo is required"}),400
    
    try:
        salary = float(salary)
    except ValueError:
        return jsonify({"msg": "salary must be a number"}),400
    
    job_image = job_photo(photo)
    if job_image["status"]==False and "msg" in job_image:
        return jsonify({"msg": job_image["msg"]}),400
    
    if job_image["status"]==True:
        image = job_image["photo"]
        
        job = Job(
            
            title = title,
            description = description,
            location = location,
            salary = salary,
            image = image,
            employer_id = employer_id
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({"status": True, "msg": "Job Created Successfully!"}),201
    
    return jsonify({"status":False, "msg": "Failed to create job"}),500
