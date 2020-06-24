from datetime import datetime
from flask import render_template, url_for, redirect, request, flash
from app import app, db, bcrypt
from app.forms import NoteForm, RegistrationForm, LoginForm
from app.models import Notes, User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET','POST'])
@login_required
def notes():
	date = datetime.now()
	results = Notes.query.all()
	return render_template('notes.html', results=results, title='Notes', legend='Notes', date=date.strftime("%A %B %d, %Y"))


@app.route('/notes/new', methods=['GET','POST'])
def create_note():
	form = NoteForm()
	if form.validate_on_submit():
		note = Notes(note=form.note.data)
		db.session.add(note)
		db.session.commit()
		flash('New note added', 'success')
		return redirect(url_for('notes'))
	return render_template('create_note.html', title='New Note',
						   form=form, legend='New Note')


@app.route("/notes/<int:id>/delete", methods=['GET','POST'])
def delete_note(id):
	note = Notes.query.get_or_404(id)
	db.session.delete(note)
	db.session.commit()
	flash('Note deleted', 'success')
	return redirect(url_for('notes'))


@app.route("/notes/<int:id>/edit", methods=['GET', 'POST'])
def edit_note(id):
	note = Notes.query.get_or_404(id)
	form = NoteForm()
	if form.validate_on_submit():
		note.note = form.note.data
		db.session.commit()
		flash('Note updated', 'success')
		return redirect(url_for('notes'))
	elif request.method == 'GET':
		form.note.data = note.note
	return render_template('create_note.html', title='Edit Note',
						   form=form, legend='Edit Note')


@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('notes'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('notes'))
		else:
			flash("Login unsuccessful", "danger")
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

#@app.route("/register", methods=['GET','POST'])
#def register():
#    if current_user.is_authenticated:
#        return redirect(url_for('notes'))
#    form = RegistrationForm()
#    if form.validate_on_submit():
#        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#        db.session.add(user)
#        db.session.commit()
#        flash(f"Registered {form.username.data}", 'success')
#        return redirect(url_for('login'))
#    return render_template('register.html', title='Register', form=form)
