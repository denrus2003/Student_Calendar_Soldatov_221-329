import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:0000@localhost/Student_Calendar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CALDAV_URL = 'https://caldav.icloud.com/'
    CALDAV_USERNAME = 'your_apple_id'
    CALDAV_PASSWORD = 'your_app_specific_password'