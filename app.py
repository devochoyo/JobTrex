from flask import Flask
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta
from extension import db
from route import register_bp, login_bp, logout_bp, refresh_bp,health_bp
from flask_migrate import Migrate


load_dotenv()
app = Flask(__name__)
migrate = Migrate(app, db)

app.json.sort_keys = False
app.register_blueprint(register_bp)
app.register_blueprint(health_bp)
#app.register_blueprint(login_bp)
#app.register_blueprint(logout_bp)
#app.register_blueprint(refresh_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['UPLOAD_FOLDER'] =  'uploads'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)