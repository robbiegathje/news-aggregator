from flask_wtf import FlaskForm
from models import Country, Language, User
from wtforms import PasswordField, SelectMultipleField, StringField

class LoginForm (FlaskForm):
	"""WTForms Login Form"""

	username = StringField('Username')
	password = PasswordField('Password')
