import os
class Config:
   class Config:
    import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://denis:0000@localhost:5432/student_calendar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CALDAV_URL = 'https://caldav.icloud.com/'
    CALDAV_USERNAME = 'your_apple_id'
    CALDAV_PASSWORD = 'your_app_specific_password'

MAIL_SERVER = 'localhost'
MAIL_PORT = 8025
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None  
MAIL_PASSWORD = None  
MAIL_DEFAULT_SENDER = 'test@example.com'