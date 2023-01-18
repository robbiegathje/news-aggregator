from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User
from secret import SECRET_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///news'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY

toolbar = DebugToolbarExtension(app)

with app.app_context():
	db.init_app(app)
