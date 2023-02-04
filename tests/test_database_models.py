# Due to SQLAlchemy detaching objects from the database when in use
# outside the traditional application view function context,
# objects must occasionally be re-retrieved amidst testing.
# You will see this noted by variable names with 'refresh' stated.

from constants import DATABASE_URL_KEY
from models import Country, db, Language, Language_Preference, Locale, User
from sqlalchemy.exc import DataError, IntegrityError
from unittest import TestCase

import os

os.environ[DATABASE_URL_KEY] = 'postgresql:///test_news'

from app import app

with app.app_context():
	db.init_app(app)
	db.drop_all()
	db.create_all()

class DatabaseModelsTestCase (TestCase):
	"""Test database models"""

	def setUp(self):
		with app.app_context():
			Language_Preference.query.delete()
			Locale.query.delete()
			User.query.delete()
			Language.query.delete()
			Country.query.delete()
			db.session.commit()
	
	def tearDown(self):
		with app.app_context():
			db.session.rollback()

	def test_user_registration(self):
		with app.app_context():
			user = User.register('testuser', 'testing')
			db.session.add(user)
			db.session.commit()

			user_refresh = User.query.filter_by(username='testuser').first()
			self.assertIsInstance(user_refresh, User)
			self.assertIsInstance(user_refresh.id, int)
			self.assertEqual(user_refresh.username, 'testuser')
			self.assertEqual(len(user_refresh.languages), 0)
			self.assertEqual(len(user_refresh.countries), 0)
			self.assertNotEqual(user_refresh.password, 'testing')
			self.assertIn('$2b$12$', user_refresh.password)

	def test_user_registration_unique_username(self):
		with app.app_context():
			user = User.register('testuser', 'testing')
			db.session.add(user)
			db.session.commit()

			nonunique_user = User.register('testuser', 'moretests')
			db.session.add(nonunique_user)
			self.assertRaises(IntegrityError, db.session.commit)

	def test_user_authenticate(self):
		with app.app_context():
			user = User.register('testuser', 'testing')
			db.session.add(user)
			db.session.commit()

			authenticated_user = User.authenticate('testuser', 'testing')
			self.assertIsInstance(authenticated_user, User)
			self.assertEqual(authenticated_user.username, 'testuser')
			self.assertIn('$2b$12$', authenticated_user.password)

	def test_user_change_password(self):
		with app.app_context():
			user = User.register('testuser', 'testing')
			db.session.add(user)
			db.session.commit()

			user_refresh = User.query.filter_by(username='testuser').first()
			current_hashed_password = user_refresh.password
			user_refresh.change_password('furthertesting')
			db.session.add(user_refresh)
			db.session.commit()

			user_with_new_password = User.query.filter_by(username='testuser').first()
			self.assertNotEqual(current_hashed_password, user_with_new_password.password)
			self.assertIn('$2b$12$', user_with_new_password.password)
			self.assertFalse(User.authenticate('testuser', 'testing'))
			self.assertIsInstance(User.authenticate('testuser', 'furthertesting'), User)

	def test_language_model(self):
		with app.app_context():
			english = Language(language='English', code='en', english_name='English')
			db.session.add(english)
			db.session.commit()

			english_refresh = Language.query.filter_by(code='en').first()
			self.assertIsInstance(english_refresh, Language)
			self.assertIsInstance(english_refresh.id, int)
			self.assertEqual(english_refresh.language, 'English')
			self.assertEqual(english_refresh.english_name, 'English')
			self.assertEqual(english_refresh.code, 'en')

	def test_language_code_character_limit(self):
		with app.app_context():
			english = Language(language='English', code='eng', english_name='English')
			db.session.add(english)
			self.assertRaises(DataError, db.session.commit)
	
	def test_language_model_unique_constraints(self):
		with app.app_context():
			english = Language(language='English', code='en', english_name='English')
			db.session.add(english)
			db.session.commit()

			nonunique_language = Language(
				language='English',
				code='eg',
				english_name='Englishish'
			)
			db.session.add(nonunique_language)
			self.assertRaises(IntegrityError, db.session.commit)
			db.session.rollback()

			nonunique_language_code = Language(
				language='English2',
				code='en',
				english_name='English2'
			)
			db.session.add(nonunique_language_code)
			self.assertRaises(IntegrityError, db.session.commit)
			db.session.rollback()

			nonunique_english_name = Language(
				language='English3',
				code='e3',
				english_name='English'
			)
			db.session.add(nonunique_english_name)
			self.assertRaises(IntegrityError, db.session.commit)
			db.session.rollback()
	
	def test_country_model(self):
		with app.app_context():
			usa = Country(country='United States Of America', code='us')
			db.session.add(usa)
			db.session.commit()

			usa_refresh = Country.query.filter_by(code='us').first()
			self.assertIsInstance(usa_refresh, Country)
			self.assertIsInstance(usa_refresh.id, int)
			self.assertEqual(usa_refresh.country, 'United States Of America')
			self.assertEqual(usa_refresh.code, 'us')

	def test_country_code_character_limit(self):
		with app.app_context():
			usa = Country(country='United States Of America', code='usa')
			db.session.add(usa)
			self.assertRaises(DataError, db.session.commit)

	def test_country_model_unique_constraints(self):
		with app.app_context():
			usa = Country(country='United States Of America', code='us')
			db.session.add(usa)
			db.session.commit()

			nonunique_country = Country(country='United States Of America', code='am')
			db.session.add(nonunique_country)
			self.assertRaises(IntegrityError, db.session.commit)
			db.session.rollback()

			nonunique_country_code = Country(country='U.S.A.', code='us')
			db.session.add(nonunique_country_code)
			self.assertRaises(IntegrityError, db.session.commit)
			db.session.rollback()
