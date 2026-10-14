import os
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CV_EXTENSIONS = ['.pdf', '.doc', '.docx']


def is_image(file):
    head = file.read(12)
    file.seek(0)
    return (head.startswith(b'\xff\xd8\xff')
            or head.startswith(b'\x89PNG')
            or head.startswith(b'GIF8')
            or head[4:8] == b'ftyp'
            or (head[:4] == b'RIFF' and head[8:12] == b'WEBP'))


def save_file(file, path):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    file.save(full_path)


def file_uploads(profile_picture, cv=None):
    
    if profile_picture and not is_image(profile_picture):
        return {
            "status": False,
            "msg": "Profile picture must be an image"
        }
    
    if cv:
        cv_ext = os.path.splitext(cv.filename)[1].lower()
        if cv_ext not in CV_EXTENSIONS:
            return {
                "status": False,
                "msg": "CV must be a PDF or Word document"
            }
    
    filename = uuid.uuid4()
    
    photo_path = None
    if profile_picture:
        photo_path = f'uploads/profile/{filename}.jpg'
        save_file(profile_picture, photo_path)
    
    if not cv:
        return{
            "status": True,
            "profile_picture": photo_path
        }
    
    cv_path = f'uploads/cv/{filename}{cv_ext}'
    save_file(cv, cv_path)
    
    return{
        "status": True,
        "profile_picture": photo_path,
        "cv": cv_path
    }

    
def job_photo(photo):
    
    if not is_image(photo):
        return {
            "status": False,
            "msg": "Job image must be an image file"
        }
    
    filename = uuid.uuid4()
    photo_path = f"uploads/jobs/{filename}.jpg"
    save_file(photo, photo_path)
    
    return {
        "status": True,
        "photo": photo_path
    }
