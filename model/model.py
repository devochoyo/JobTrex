from extension import db
from enum import Enum

class UserRole(Enum):
    ADMIN = 'admin'
    EMPLOYER = 'employer'
    APPLICANT = 'applicant'
    
    
class JobStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True)
    role = db.Column(
        db.Enum(
            UserRole, 
            name ="userrole", values_callable=lambda x: [e.value for e in x]), default=UserRole.APPLICANT
        )
    password = db.Column(db.Text, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    cv = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    
class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=True)
    image = db.Column(db.Text, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employer = db.relationship('User', backref=db.backref('jobs', lazy=True))
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    
class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    applicant = db.relationship('User', backref=db.backref('applications', lazy=True))
    status = db.Column(
        db.Enum(
            JobStatus, name="jobstatus", values_callable=lambda x: [e.value for e in x]),
        default=JobStatus.PENDING)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
class Revoke(db.Model):
    __tablename__ = 'revoke'
        
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.Text, unique=True, nullable=False)

class OTP(db.Model):
    __tablename__='otp'
    
    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    expire_at = db.Column(db.DateTime(timezone=True), nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())