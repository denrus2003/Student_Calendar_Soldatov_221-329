from flask_wtf import FlaskForm
from wtforms import DateTimeField, FileField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
from flask_wtf.file import FileAllowed
from wtforms.fields import DateField, TimeField
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Запросить сброс пароля')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EventForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    date = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Время начала', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('Время окончания', format='%H:%M', validators=[DataRequired()])
    attachment = FileField('Загрузить файл', validators=[Optional(), FileAllowed(['jpg', 'png', 'pdf', 'docx'], 'Только изображения и документы')])
    submit = SubmitField('Создать событие')

class ShowEventForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    date = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Время начала', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('Время окончания', format='%H:%M', validators=[DataRequired()])
    attachment = FileField('Вложение')  # Добавляем поле attachment
    submit = SubmitField('Сохранить изменения')