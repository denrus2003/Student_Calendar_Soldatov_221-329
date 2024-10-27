from datetime import datetime
import os
import logging
import secrets
from flask import Flask, abort, render_template, flash, redirect, url_for, request, session, current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Message
from urllib.parse import urlparse

from . import db
from app.forms import EventForm, LoginForm, RegistrationForm, ShowEventForm, ResetPasswordForm, RequestResetForm
from .models import User, Event
from .gcalendar import create_google_event, get_calendar_service
from .apple_calendar import create_event as create_apple_event
from app import mail

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

UPLOAD_FOLDER = '/Users/denis/Downloads/Учеба/Студентческий_календарь/app/static/uploads'

@app.route('/')
@app.route('/index')
@login_required
def index():
    print(f"ID аутендифицированного пользователя: {current_user.id}")
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', title='Главная', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Недействительный или истекший токен', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был обновлен! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Если эта почта зарегистрирована, мы отправили ссылку для сброса пароля.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    session.pop('_flashes', None)
    if form.validate_on_submit():
        try:
            # Получаем данные из формы
            title = form.title.data
            date = form.date.data
            start_time = form.start_time.data
            end_time = form.end_time.data
            description = form.description.data
            attachment = form.attachment.data

            # Сохранение файла, если он загружен
            filename = None
            if attachment:
                filename = secure_filename(attachment.filename)
                attachment.save(os.path.join(UPLOAD_FOLDER, filename))

            # Объединяем дату и время для хранения в базе данных
            start_datetime = datetime.combine(date, start_time)
            end_datetime = datetime.combine(date, end_time)

            # Создаем объект события
            event = Event(
                title=title,
                start_time=start_datetime,
                end_time=end_datetime,
                description=description,
                date=date,
                attachment=filename,
                user_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()

            # Синхронизация с Google Календарем
            google_event_id = create_google_event(event)
            if google_event_id:
                event.google_event_id = google_event_id

            # Синхронизация с Apple Календарем (передаем start и end)
            create_apple_event(event, start=start_datetime, end=end_datetime)

            db.session.commit()
            flash('Событие успешно создано и добавлено в внешние календари.', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            logging.error(f'Ошибка при создании события: {e}')
            flash(f'Не удалось создать событие. Ошибка: {e}', 'danger')

    return render_template('create_event.html', title='Создать событие', form=form)

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        abort(403)

    form = ShowEventForm(obj=event)

    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.start_time = datetime.combine(form.date.data, form.start_time.data)
        event.end_time = datetime.combine(form.date.data, form.end_time.data)

        if form.attachment.data:
            try:
                filename = secure_filename(form.attachment.data.filename)
                form.attachment.data.save(os.path.join(UPLOAD_FOLDER, filename))
                event.attachment = filename
            except Exception as e:
                logging.error(f'Ошибка при сохранении вложения: {e}')
        
        try:
            db.session.commit()
            flash('Событие успешно изменено.', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Ошибка при обновлении события: {e}')
            flash(f'Ошибка при сохранении изменений: {e}', 'danger')

        return redirect(url_for('index'))
    
    return render_template('event.html', title='Редактировать событие', form=form, event=event)

@app.route('/view_event/<int:id>', methods=['GET'])
@login_required
def view_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        abort(403)
    return render_template('view_event.html', title=event.title, event=event)

@app.route('/delete_event/<int:id>', methods=['POST'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        abort(403)
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Событие удалено.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении события: {e}', 'danger')
    return redirect(url_for('index'))

@app.route('/add_to_google/<int:event_id>', methods=['GET'])
@login_required
def add_to_google(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    try:
        create_google_event(event)
        flash('Событие добавлено в Google Календарь.', 'success')
    except Exception as e:
        logging.error(f'Ошибка при добавлении события в Google Календарь: {e}')
        flash(f'Не удалось добавить событие в Google Календарь: {e}', 'danger')
    return redirect(url_for('index'))

@app.route('/add_to_apple/<int:event_id>', methods=['GET'])
@login_required
def add_to_apple(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    try:
        # Передача start и end для синхронизации с Apple Календарем
        create_apple_event(event, start=event.start_time, end=event.end_time)
        flash('Событие добавлено в Apple Календарь.', 'success')
    except Exception as e:
        logging.error(f'Ошибка при добавлении события в Apple Календарь: {e}')
        flash(f'Не удалось добавить событие в Apple Календарь: {e}', 'danger')
    return redirect(url_for('index'))

@app.route('/add_all_to_google', methods=['GET'])
@login_required
def add_all_to_google():
    events = Event.query.filter_by(user_id=current_user.id).all()
    try:
        for event in events:
            google_event_id = create_google_event(event)
            if google_event_id:
                event.google_event_id = google_event_id
        db.session.commit()
        flash('Все события добавлены в Google Календарь.', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f'Ошибка при добавлении всех событий в Google Календарь: {e}')
        flash(f'Не удалось добавить все события в Google Календарь: {e}', 'danger')
    return redirect(url_for('index'))

@app.route('/add_all_to_apple', methods=['GET'])
@login_required
def add_all_to_apple():
    events = Event.query.filter_by(user_id=current_user.id).all()
    try:
        for event in events:
            create_apple_event(event, start=event.start_time, end=event.end_time)
        flash('Все события добавлены в Apple Календарь.', 'success')
    except Exception as e:
        logging.error(f'Ошибка при добавлении всех событий в Apple Календарь: {e}')
        flash(f'Не удалось добавить все события в Apple Календарь: {e}', 'danger')
    return redirect(url_for('index'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f'''Для сброса пароля перейдите по следующей ссылке:
{url_for('reset_token', token=token, _external=True)}

Если вы не запрашивали сброс пароля, проигнорируйте это письмо.
'''
    mail.send(msg)