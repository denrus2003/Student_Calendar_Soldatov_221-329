from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time, date
from . import db
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from hashlib import sha256
import os

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    events = db.relationship('Event', backref='user', lazy=True)
    salt = db.Column(db.String(32), nullable=False, default=lambda: sha256(os.urandom(60)).hexdigest()[:32])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def get_reset_token(self, expires_sec=1800):
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
            
        salt = self.salt
        if isinstance(salt, int):
            salt = str(salt).encode('utf-8')
        elif isinstance(salt, str):
            salt = salt.encode('utf-8')
    
        s = Serializer(secret_key, expires_sec)
        s.salt = salt
        return s.dumps({'user_id': self.id})  # Убираем .decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        
        s = Serializer(secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    date = db.Column(db.Date, nullable=False)
    attachment = db.Column(db.String(100), nullable=True)

class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)