from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

class User (db.Model):
	"""SQLAlchemy User Model"""

	__tablename__ = 'users'
	id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)
	languages = db.relationship('Language', secondary='language_preferences')
	countries = db.relationship('Country', secondary='locales')

	@classmethod
	def register(cls, username, password):
		hashed = bcrypt.generate_password_hash(password)
		hashed_utf8 = hashed.decode('utf8')
		return cls(
			username=username,
			password=hashed_utf8
		)
	
	@classmethod
	def authenticate(cls, username, password):
		user = User.query.filter(User.username.ilike(username)).first()
		if user and bcrypt.check_password_hash(user.password, password):
			return user
		return False
	
	def add_new_languages(self, language_code_list):
		for language_code in language_code_list:
			language = Language.query.filter_by(code=language_code).first()
			self.languages.append(language)

	def add_new_countries(self, country_code_list):
		for country_code in country_code_list:
			country = Country.query.filter_by(code=country_code).first()
			self.countries.append(country)

	def change_password(self, new_password):
		hashed = bcrypt.generate_password_hash(new_password)
		hashed_utf8 = hashed.decode('utf8')
		self.password = hashed_utf8

class Language (db.Model):
	"""SQLAlchemy Language Model"""

	__tablename__ = 'languages'
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(2), unique=True, nullable=False)
	english_name = db.Column(db.String(), unique=True, nullable=False)
	language = db.Column(db.String(), unique=True, nullable=False)

class Country (db.Model):
	"""SQLAlchemy Country Model"""

	__tablename__ = 'countries'
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(2), unique=True, nullable=False)
	country = db.Column(db.String(), unique=True, nullable=False)

class Language_Preference (db.Model):
	"""SQLAlchemy Language_Preference Model"""

	__tablename__ = 'language_preferences'
	id = db.Column(db.Integer(), primary_key=True)
	language_id = db.Column(
		db.Integer(),
		db.ForeignKey('languages.id'),
		nullable=False
	)
	user_id = db.Column(
		db.Integer(),
		db.ForeignKey('users.id'),
		nullable=False
	)
	__table_args__ = (db.UniqueConstraint(
		'language_id',
		'user_id',
		name='unique_lang_user_pair'),
	)

class Locale (db.Model):
	"""SQLAlchemy Locale Model"""

	__tablename__ = 'locales'
	id = db.Column(db.Integer(), primary_key=True)
	country_id = db.Column(
		db.Integer(),
		db.ForeignKey('countries.id'),
		nullable=False
	)
	user_id = db.Column(
		db.Integer(),
		db.ForeignKey('users.id'),
		nullable=False
	)
	__table_args__ = (db.UniqueConstraint(
		'country_id',
		'user_id',
		name='unique_country_user_pair'),
	)
