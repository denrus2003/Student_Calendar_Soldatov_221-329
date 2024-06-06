from os import abort
from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import EventForm, LoginForm, RegistrationForm
from app.models import Event, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.gcalendar import create_google_event

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home')

def create_event():
    form = EventForm()
    if form.validate_on_submit():
        filename = None
        if form.attachment.data:
            filename = secure_filename(form.attachment.data.filename)
            form.attachment.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            attachment=filename,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        create_google_event(event) 
        flash('Event created successfully.')
        return redirect(url_for('index'))
    return render_template('event.html', title='Create Event', form=form)

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        if form.attachment.data:
            filename = secure_filename(form.attachment.data.filename)
            form.attachment.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            event.attachment = filename
        event.title = form.title.data
        event.description = form.description.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        db.session.commit()
        flash('Event updated successfully.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.start_time.data = event.start_time
        form.end_time.data = event.end_time
    return render_template('event.html', title='Edit Event', form=form)