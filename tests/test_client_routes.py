# Due to SQLAlchemy detaching objects from the database when in use
# outside the traditional application view function context,
# objects must occasionally be re-retrieved amidst testing.
# You will see this noted by variable names with 'refresh' stated.

from constants import *
from models import Country, db, Language, Language_Preference, Locale, User
from unittest import TestCase

import os

os.environ[DATABASE_URL_KEY] = 'postgresql:///test_news'

from app import app

app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
	db.init_app(app)
	db.drop_all()
	db.create_all()

class UserStatusRoutesTestCase (TestCase):
	"""Test home, login, register, & logout routes"""

	def setUp(self):
		with app.app_context():
			Language_Preference.query.delete()
			Locale.query.delete()
			User.query.delete()
			Language.query.delete()
			Country.query.delete()
			db.session.commit()

			user = User.register('testuser', 'testing')
			db.session.add(user)
			db.session.commit()

			english = Language(language='English', code='en', english_name='English')
			spanish = Language(code='es', english_name='Spanish', language='Español')
			db.session.add_all([english, spanish])
			db.session.commit()

			usa = Country(country='United States Of America', code='us')
			mexico = Country(code='mx', country='Mexico')
			db.session.add_all([usa, mexico])
			db.session.commit()

			user_refresh = User.query.filter_by(username='testuser').first()
			user_refresh.add_new_languages(['en', 'es'])
			user_refresh.add_new_countries(['us', 'mx'])
			db.session.add(user_refresh)
			db.session.commit()

		self.client = app.test_client()
	
	def test_show_home_experience_logged_out(self):
		with self.client as client:
			response = client.get('/')
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/login')

	def test_show_home_experience_logged_in(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/')
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')
	
	def test_get_login(self):
		with self.client as client:
			response = client.get('/login')
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)

	def test_post_login(self):
		with self.client as client:
			response = client.post('/login', data={'username': 'testuser', 'password': 'testing'})
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')
			user = User.query.filter_by(username='testuser').first()
			with client.session_transaction() as session:
				self.assertEqual(session[CURR_USER_KEY], user.id)
	
	def test_login_invalid_user(self):
		with self.client as client:
			response = client.post(
				'/login',
				data={'username': 'notauser', 'password': 'testing'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn('Username &#34;notauser&#34; does not exist.', html)

	def test_login_incorrect_password(self):
		with self.client as client:
			response = client.post(
				'/login',
				data={'username': 'testuser', 'password': 'thisiswrong'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn(INCORRECT_PASSWORD_MESSAGE, html)
	
	def test_login_already_logged_in(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/login')
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')

class EditUserRoutesTestCase (TestCase):
	"""Test routes related to editing the user and their preferences"""

	def setUp(self):
		self.client = app.test_client()

class NewsRoutesTestCase (TestCase):
	"""Test routes related to displaying news articles"""

	def setUp(self):
		self.client = app.test_client()
