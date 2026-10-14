from flask import jsonify
from werkzeug.security import generate_password_hash
from model.model import User
from extension import db
from uploads import file_uploads
from auth.validate import validate


def applicant_reg(firstname, lastname, email, password, role, country,profile_picture, cv):
    
    if firstname is None:   
        return jsonify({'msg': 'Firstname is required'}), 400
    if lastname is None:
        return jsonify({'msg': 'Lastname is required'}), 400
    if email is None:
        return jsonify({'msg': 'Email is required'}), 400
    if password is None:
        return jsonify({'msg': 'Password is required'}), 400
    if role is None:
        return jsonify({'msg': 'Role is required'}), 400
    if country is None:
        return jsonify({'msg': 'Country is required'}), 400
    if cv is None:
        return jsonify({'msg': 'CV is required'}), 400
    
    firstname = firstname.strip()
    lastname = lastname.strip()
    email = email.strip()
    password = password.strip()
    country = country.strip()

    
    if not firstname:
        return jsonify({'msg': 'Firstname cannot be empty'}), 400
    if not lastname:
        return jsonify({'msg': 'Lastname cannot be empty'}), 400
    if not email:
        return jsonify({'msg': 'Email cannot be empty'}), 400
    if not password:
        return jsonify({'msg': 'Password cannot be empty'}), 400
    if not role:
        return jsonify({'msg': 'Role cannot be empty'}), 400
    if not country:
        return jsonify({'msg': 'Country cannot be empty'}), 400
    if not cv:
        return jsonify({'msg': 'CV cannot be empty'}), 400
    
    if role == 'admin':
        return jsonify({'msg': 'You cannot register as an admin'}), 400
    if role == 'employer':
        return jsonify({'msg': 'You cannot register as an employer'}), 400
    
    validate_email = validate(email)
    
    if validate_email:
        return jsonify({'msg': 'Email already exists'}), 400
    
    if len(password) < 6:
        return jsonify({'msg': 'Password must be at least 6 characters long'}), 400
    
    if '@' not in email or '.' not in email:
        return jsonify({'msg': 'Invalid email format'}), 400
    
    hashed_password = generate_password_hash(password)
    
    
    res = file_uploads(profile_picture, cv)
    if res['status'] == False and 'msg' in res:
        return jsonify({'msg': res['msg']}), 400
    
    if res['status'] == True:
        photo_path = res['profile_picture']
        cv_path = res['cv']
    
        user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            role=role,
            country=country,
            password=hashed_password,
            profile_picture=photo_path,
            cv=cv_path
        )
        db.session.add(user)
        db.session.commit()
    
        return jsonify({
            "status": True,
            'msg': 'Registration successful!'
            }), 201
    
    return jsonify({
        "status": False,
        'msg': 'Registration failed!'
        }), 500
    

def employer_reg(firstname, lastname, email, password, role, country,profile_picture):
    
    if firstname is None:   
        return jsonify({'msg': 'Firstname is required'}), 400
    if lastname is None:
        return jsonify({'msg': 'Lastname is required'}), 400
    if email is None:
        return jsonify({'msg': 'Email is required'}), 400
    if password is None:
        return jsonify({'msg': 'Password is required'}), 400
    if role is None:
        return jsonify({'msg': 'Role is required'}), 400
    if country is None:
        return jsonify({'msg': 'Country is required'}), 400

    
    firstname = firstname.strip()
    lastname = lastname.strip()
    email = email.strip()
    password = password.strip()
    country = country.strip()
    
    if not firstname:
        return jsonify({'msg': 'Firstname cannot be empty'}), 400
    if not lastname:
        return jsonify({'msg': 'Lastname cannot be empty'}), 400
    if not email:
        return jsonify({'msg': 'Email cannot be empty'}), 400
    if not password:
        return jsonify({'msg': 'Password cannot be empty'}), 400
    if not role:
        return jsonify({'msg': 'Role cannot be empty'}), 400
    if not country:
        return jsonify({'msg': 'Country cannot be empty'}), 400
    if role == 'admin':
        return jsonify({'msg': 'You cannot register as an admin'}), 400
    if role == 'applicant':
        return jsonify({'msg': 'You cannot register as an applicant'}), 400
    
    validate_email = validate(email)
    if validate_email:
        return jsonify({'msg': 'Email already exists'}), 400
    
    if len(password) < 6:
        return jsonify({'msg': 'Password must be at least 6 characters long'}), 400
    
    if '@' not in email or '.' not in email:
        return jsonify({'msg': 'Invalid email format'}), 400
    
    hashed_password = generate_password_hash(password)
    

    
    res = file_uploads(profile_picture)
    if res['status'] == False and 'msg' in res:
        return jsonify({'msg': res['msg']}), 400
    
    if res['status'] == True:
        photo_path = res['profile_picture']
        
        user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            role=role,
            country=country,
            password=hashed_password,
            profile_picture=photo_path
        )
    
        db.session.add(user)
        db.session.commit()
    
        return jsonify({
            "status": True,
            'msg': 'Registration successful!'
            }), 201
    return jsonify({
        "status": False,
        'msg': 'Registration failed!'
        }), 500

    
    
    

    

    
