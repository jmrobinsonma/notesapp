from datetime import datetime
from flask import render_template, url_for, redirect, request, flash
from app import app, db, bcrypt
from app.forms import NoteForm, RegistrationForm, LoginForm
from app.models import Notes, User
from flask_login import login_user, current_user, logout_user, login_required

date = datetime.now().strftime("%A %B %d, %Y")

@app.route("/", methods=['GET','POST'])
@login_required
def notes():
	results = Notes.query.all()
	note_button = True
	return render_template(
		'notes.html', 
		results=results, 
		title='Notes', 
		legend='Notes', 
		date=date
	)


@app.route('/notes/new', methods=['GET','POST'])
def create_note():
	form = NoteForm()
	if form.validate_on_submit():
		note = Notes(note=form.note.data)
		db.session.add(note)
		db.session.commit()
		return redirect(url_for('notes'))
	elif request.method == 'GET':
		return render_template(
			'create_note.html', 
			title='New Note',
			form=form, 
			legend='New Note',
			date=date
		)


@app.route("/notes/<int:id>/delete", methods=['GET','POST'])
def delete_note(id):
	note = Notes.query.get_or_404(id)
	db.session.delete(note)
	db.session.commit()
	return redirect(url_for('notes'))


@app.route("/notes/<int:id>/edit", methods=['GET', 'POST'])
def edit_note(id):
	note = Notes.query.get_or_404(id)
	form = NoteForm()
	if form.validate_on_submit():
		note.note = form.note.data
		db.session.commit()
		return redirect(url_for('notes'))
	elif request.method == 'GET':
		form.note.data = note.note
	return render_template(
		'create_note.html', 
		title='Edit Note',
		form=form, 
		legend='Edit Note',
		date=date
	)


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


#@app.route("/login")
#def login():
#    # Find out what URL to hit for Google login
#    google_provider_cfg = get_google_provider_cfg()
#    authorization_endpoint = google_provider_cfg["authorization_endpoint"]#

#    # Use library to construct the request for login and provide
#    # scopes that let you retrieve user's profile from Google
#    request_uri = client.prepare_request_uri(
#        authorization_endpoint,
#        redirect_uri="https://127.0.0.1:5000/login/callback",
#        scope=["openid", "email", "profile"],
#    )
#    return redirect(request_uri)#

#@app.route("/login/callback")
#def callback():
#    # Get authorization code Google sent back to you
#    code = request.args.get("code")#

#    # Find out what URL to hit to get tokens that allow you to ask for
#    # things on behalf of a user
#    google_provider_cfg = get_google_provider_cfg()
#    token_endpoint = google_provider_cfg["token_endpoint"]#

#    # Prepare and send request to get tokens! Yay tokens!
#    token_url, headers, body = client.prepare_token_request(
#        token_endpoint,
#        authorization_response=request.url,
#        redirect_url=request.base_url,
#        code=code,
#    )
#    token_response = requests.post(
#        token_url,
#        headers=headers,
#        data=body,
#        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#    )#

#    # Parse the tokens!
#    client.parse_request_body_response(json.dumps(token_response.json()))#

#    # Now that we have tokens (yay) let's find and hit URL
#    # from Google that gives you user's profile information,
#    # including their Google Profile Image and Email
#    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#    uri, headers, body = client.add_token(userinfo_endpoint)
#    userinfo_response = requests.get(uri, headers=headers, data=body)#

#    # We want to make sure their email is verified.
#    # The user authenticated with Google, authorized our
#    # app, and now we've verified their email through Google!
#    if userinfo_response.json().get("email_verified"):
#        unique_id = userinfo_response.json()["sub"]
#        users_email = userinfo_response.json()["email"]
#        picture = userinfo_response.json()["picture"]
#        users_name = userinfo_response.json()["given_name"]
#    else:
#        return "User email not available or not verified by Google.", 400#

#    # Create a user in our db with the information provided
#    # by Google
#    user = User(
#        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
#    )#

#    # Doesn't exist? Add to database
#    if not User.get(unique_id):
#        User.create(unique_id, users_name, users_email, picture)#

#    # Begin user session by logging the user in
#    login_user(user)#

#    # Send user back to homepage
#    return redirect(url_for("index"))#

#def get_google_provider_cfg():
#    return requests.get(GOOGLE_DISCOVERY_URL).json()