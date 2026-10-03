def file_uploads(profile_picture, cv):
      photo_path = f'uploads/profile/{profile_picture.filename}'
      cv_path = f'uploads/cv/{cv.filename}'
      
      profile_picture.save(photo_path)
      cv.save(cv_path)
      
      return True