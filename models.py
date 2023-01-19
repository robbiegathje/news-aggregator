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

	@classmethod
	def register(cls, username, password):
		hashed = bcrypt.generate_password_hash(password)
		hashed_utf8 = hashed.decode('utf8')
		return cls(
			username=username,
			password=hashed_utf8
		)
	
	@classmethod
	def login(cls, username, password):
		user = User.query.filter_by(username=username).first()
		if user and bcrypt.check_password_hash(user.password, password):
			return user
		return False

class Language (db.Model):
	"""SQLAlchemy Language Model"""

	__tablename__ = 'languages'
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(2), unique=True, nullable=False)
	language = db.Column(db.String(), unique=True, nullable=False)

class Country (db.Model):
	"""SQLAlchemy Country Model"""

	__tablename__ = 'countries'
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(2), unique=True, nullable=False)
	country = db.Column(db.String(), unique=True, nullable=False)
