from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
#from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
app.config['SECRET_KEY'] = "0d9ffa033dba18831e5575a9e8d25580"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

# Configuration
#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
#GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
#GOOGLE_DISCOVERY_URL = (
#    "https://accounts.google.com/.well-known/openid-configuration"
#)


from app import routes

csrf = CsrfProtect(app)
csrf.init_app(app)
