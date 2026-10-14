from flask import Flask,send_from_directory
from flask_jwt_extended import verify_jwt_in_request
import os
from dotenv import load_dotenv
from datetime import timedelta
from extension import db,jwt,mail
from route import (register_bp,
                   login_bp,
                   logout_bp,
                   refresh_bp,
                   health_bp,
                   forgotten_password_bp,
                   verify_bp,reset_bp,
                   create_job_bp,
                   employer_jobs_bp,
                   apply_bp,
                   applicant_bp,
                   employ_bp,
                   employed_bp,
                   jobs_bp,
                   job_details_bp,
                   my_applications_bp,
                   withdraw_bp,
                   reject_bp,
                   edit_job_bp,
                   delete_job_bp,
                   applicant_profile_bp,
                   profile_bp,
                   update_profile_bp,
                   change_password_bp,
                   send_verification_bp,
                   verify_email_bp
                   )

from flask_migrate import Migrate


load_dotenv()
app = Flask(__name__)
migrate = Migrate(app, db)


@app.route("/uploads/<path:filepath>")
def get_file(filepath):
    folder = 'uploads'
    
    if filepath.startswith('cv/'):
        verify_jwt_in_request()
    
    return send_from_directory(folder, filepath)




app.json.sort_keys = False
app.register_blueprint(register_bp)
app.register_blueprint(health_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(refresh_bp)
app.register_blueprint(forgotten_password_bp)
app.register_blueprint(verify_bp)
app.register_blueprint(reset_bp)
app.register_blueprint(create_job_bp)
app.register_blueprint(employer_jobs_bp)
app.register_blueprint(apply_bp)
app.register_blueprint(applicant_bp)
app.register_blueprint(employ_bp)
app.register_blueprint(employed_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(job_details_bp)
app.register_blueprint(my_applications_bp)
app.register_blueprint(withdraw_bp)
app.register_blueprint(reject_bp)
app.register_blueprint(edit_job_bp)
app.register_blueprint(delete_job_bp)
app.register_blueprint(applicant_profile_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(update_profile_bp)
app.register_blueprint(change_password_bp)
app.register_blueprint(send_verification_bp)
app.register_blueprint(verify_email_bp)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['UPLOAD_FOLDER'] =  'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

if not app.config['SQLALCHEMY_DATABASE_URI'] or not app.config['JWT_SECRET_KEY']:
    raise RuntimeError('DATABASE_URL and JWT_SECRET_KEY must be set in .env')

#mail configuration
app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = os.getenv('SENDER')
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')


jwt.init_app(app)
db.init_app(app)
mail.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)