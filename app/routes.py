import datetime
from flask import Flask, abort, render_template, flash, redirect, url_for, request, current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from . import db
from app.forms import EventForm, LoginForm, RegistrationForm
from .models import User, Event, Attachment
from werkzeug.security import generate_password_hash
from .gcalendar import create_google_event, get_calendar_service, create_event
from .apple_calendar import create_event as create_apple_event

@app.route('/')
@app.route('/index')
@login_required
def index():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', title='Home', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        title = form.title.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        description = form.description.data
        attachment = form.attachment.data  # если вы хотите обработать вложение
        event = Event(title=title, start_time=start_time, end_time=end_time, description=description, user_id=current_user.id)
        db.session.add(event)
        db.session.commit()

        # Create event in Google Calendar
        service = get_calendar_service()
        event_data = {
            'summary': title,
            'description': description,
            'start': {'dateTime': start_time},
            'end': {'dateTime': end_time},
        }
        create_google_event(service, event_data)

        # Create event in Apple Calendar
        create_apple_event(title, start_time, end_time, description)

        return redirect(url_for('index'))
    return render_template('event.html', title='Create Event', form=form)

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        abort(403)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.description = form.description.data
        attachment = form.attachment.data  # если вы хотите обработать вложение
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event.html', title='Edit Event', form=form)
@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, description=form.description.data, date=form.date.data, user_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_event.html', title='Create Event', form=form)
