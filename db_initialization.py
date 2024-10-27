from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost/Student_Calendar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models here to ensure they are registered with SQLAlchemy
from models import User

def create_app():
    with app.app_context():
        db.create_all()
    return app