from constants import INVALID_USERNAME_MESSAGE, INVALID_PASSWORD_MESSAGE, PASSWORD_REGEXP, USERNAME_REGEXP
from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectMultipleField, StringField
from wtforms.validators import InputRequired, Length, Regexp

class LoginForm (FlaskForm):
	"""WTForms Login Form"""

	username = StringField('Username', validators=[InputRequired()])
	password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm (FlaskForm):
	"""WTForms Registration Form"""

	username = StringField(
		'Username',
		validators=[
			InputRequired(),
			Length(min=4, max=20),
			Regexp(USERNAME_REGEXP, message=INVALID_USERNAME_MESSAGE)
		]
	)
	password = PasswordField(
		'Password',
		validators=[
			InputRequired(),
			Length(min=8),
			Regexp(PASSWORD_REGEXP, message=INVALID_PASSWORD_MESSAGE)
		]
	)
	languages = SelectMultipleField('Languages - optional')
	countries = SelectMultipleField('Countries - optional')

class UserPreferencesForm (FlaskForm):
	"""WTForms User Preferences Form"""

	languages = SelectMultipleField('Languages', validators=[InputRequired()])
	countries = SelectMultipleField('Countries - optional')

class UsernameChangeForm (FlaskForm):
	"""WTForms Username Change Form"""

	username = StringField(
		'New Username',
		validators=[
			InputRequired(),
			Length(min=4, max=20),
			Regexp(USERNAME_REGEXP, message=INVALID_USERNAME_MESSAGE)
		]
	)

	password = PasswordField(
		'Confirm Password',
		validators=[InputRequired()]
	)

class PasswordChangeForm (FlaskForm):
	"""WTForms Password Change Form"""

	current_password = PasswordField(
		'Current Password',
		validators=[InputRequired()]
	)
	new_password = PasswordField(
		'New Password',
		validators=[
			InputRequired(),
			Length(min=8),
			Regexp(PASSWORD_REGEXP, message=INVALID_PASSWORD_MESSAGE)
		]
	)
	confirm_new_password = PasswordField(
		'Confirm New Password',
		validators=[InputRequired()]
	)
