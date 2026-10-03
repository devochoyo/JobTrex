import random

def file_uploads(profile_picture, cv):
    
    prefix = random.randint(1000, 9999)
    
    photo_path = f'uploads/profile/{prefix}_{profile_picture.filename}'
    cv_path = f'uploads/cv/{prefix}_{cv.filename}'
      
    profile_picture.save(photo_path)
    cv.save(cv_path)
      
    return{
        "status": True,
        "profile_picture": photo_path,
        "cv": cv_path
    }