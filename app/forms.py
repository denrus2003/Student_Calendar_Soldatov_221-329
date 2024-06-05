from flask_login import current_user, login_required
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField 
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo 
from app.models import Event, User
from wtforms.validators import Length 
from flask import abort, app, flash, redirect, render_template, request, url_for
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

from wtforms import DateTimeField 

from wtforms import TextAreaField 
from app import db

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=400)])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Submit')
    attachment = FileField('Attachment', validators=[FileAllowed(['jpg', 'png', 'pdf', 'docx'])])
    def create_event():
        form = EventForm()
        if form.validate_on_submit():
            event = Event(
                title=form.title.data,
                description=form.description.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                user_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully.')
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    def create_event():
        form = EventForm()
        if form.validate_on_submit():
            event = Event(
                title=form.title.data,
                description=form.description.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                user_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()
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

@app.route('/delete_event/<int:id>', methods=['POST'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully.')
    return redirect(url_for('index'))