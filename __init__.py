from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os
from flask_login import LoginManager

# Инициализация объектов
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Инициализация расширений
    db.init_app(app)  
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Убедитесь, что модели импортированы перед созданием таблиц
        from . import routes, models  
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))