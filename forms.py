from flask_wtf import FlaskForm
from models import Country, Language, User
from wtforms import PasswordField, SelectMultipleField, StringField
from wtforms.validators import InputRequired, Length

class LoginForm (FlaskForm):
	"""WTForms Login Form"""

	username = StringField('Username', validators=[InputRequired()])
	password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm (FlaskForm):
	"""WTForms Login Form"""

	username = StringField(
		'Username',
		validators=[InputRequired(), Length(min=4, max=20)]
	)
	password = PasswordField(
		'Password',
		validators=[InputRequired(), Length(min=8)]
	)
	languages = SelectMultipleField('Languages', validators=[InputRequired()])
	countries = SelectMultipleField('Countries')
