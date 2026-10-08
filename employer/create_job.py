from model.model import Job
from flask import jsonify
from extension import db
from uploads import job_photo

def create_job(title, description, location, salary, photo, employer_id):
    
    if not title:
        return jsonify({"msg": "title is required"}),400
    
    if not description:
        return jsonify({"msg": "description is required"}),400
    
    if not location:
        return jsonify({"msg": "location is required"}),400
    
    if not salary:
        return jsonify({"msg": "Job image is required"}),400

    if not photo:
        return jsonify({"msg": "job photo is required"}),400
    
    if title is None:
        return jsonify({"msg":"title cannot be empty"}),400
    
    if description is None:
        return jsonify({"msg":"description cannot be empty"}),400
    
    if salary is None:
        return jsonify({"msg":"salary cannot be empty"}),400
    
    if location is None:
        return jsonify({"msg":"location cannot be empty"}),400
    
    if photo is None:
        return jsonify({"msg":"Job image cannot be empty"}),400
    
    job_image = job_photo(photo)
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
        

    
    
    

    
   
    
