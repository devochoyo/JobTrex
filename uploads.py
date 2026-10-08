import uuid

def file_uploads(profile_picture, cv=None):
    
    filename = uuid.uuid4()
    
    photo_path = f'uploads/profile/{filename}.jpg'
    if cv is not None:
        cv_path = f'uploads/cv/{filename}.jpg'
    
      
    profile_picture.save(photo_path)
    if cv is not None:
        cv.save(cv_path)
    
    
    if cv is None:
        return{
            "status": True,
            "profile_picture": photo_path
        }
    return{
        "status": True,
        "profile_picture": photo_path,
        "cv": cv_path
    }

    
def job_photo(photo):
    filename = uuid.uuid4()
    photo = photo
    photo_path = f"uploads/jobs/{filename}.jpg"
    photo.save(photo_path)
    
    return {
        "status": True,
        "photo": photo_path
    }
        
        
        