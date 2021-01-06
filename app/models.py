from flask_sqlalchemy import SQLAlchemy
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Notes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	note = db.Column(db.String())

	def __repr__(self):
		return f"{self.id} {self.note}"

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=False, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"{self.id} {self.username} {self.email} {self.password}"
		