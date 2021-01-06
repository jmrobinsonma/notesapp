import os
from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = "0d9ffa033dba18831e5575a9e8d25580" #os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///notes.db" #os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)

from app import routes

csrf = CsrfProtect(app)
csrf.init_app(app)
