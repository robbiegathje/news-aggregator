# Due to SQLAlchemy detaching objects from the database when in use
# outside the traditional application view function context,
# objects must occasionally be re-retrieved amidst testing.
# You will see this noted by variable names with 'refresh' stated.

from constants import *
from models import Country, db, Language, Language_Preference, Locale, User
from unittest import TestCase

import os

os.environ['DATABASE_URL'] = 'postgresql:///test_news'

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

			user = User.register('testuser', 'usedintesting')
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
			response = client.post(
				'/login',
				data={'username': 'testuser', 'password': 'usedintesting'}
			)
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')
			user = User.query.filter_by(username='testuser').first()
			with client.session_transaction() as session:
				self.assertEqual(session[CURR_USER_KEY], user.id)
	
	def test_login_invalid_user(self):
		with self.client as client:
			response = client.post(
				'/login',
				data={'username': 'notauser', 'password': 'usedintesting'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn('Username &#34;notauser&#34; does not exist.', html)
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)

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
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)
	
	def test_login_already_logged_in(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/login')
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')
	
	def test_get_register(self):
		with self.client as client:
			response = client.get('/register')
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>REGISTER</b></h2>', html)
	
	def test_post_register_without_preferences(self):
		with self.client as client:
			response = client.post(
				'/register',
				data={'username': 'secondtestuser', 'password': 'moretesting'}
			)
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')
			new_user = User.query.filter_by(username='secondtestuser').first()
			english = Language.query.filter_by(language='English').first()
			self.assertEqual(new_user.languages, [english])
			self.assertEqual(len(new_user.countries), 0)
			with client.session_transaction() as session:
				self.assertEqual(session[CURR_USER_KEY], new_user.id)
	
	def test_post_register_with_preferences(self):
		with self.client as client:
			response = client.post(
				'/register',
				data={
					'username': '2nd_testuser',
					'password': 'moretesting',
					'languages': ['en', 'es'],
					'countries': ['us', 'mx']
				}
			)
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')
			new_user = User.query.filter_by(username='2nd_testuser').first()
			english = Language.query.filter_by(language='English').first()
			spanish = Language.query.filter_by(english_name='Spanish').first()
			usa = Country.query.filter_by(country='United States Of America').first()
			mexico = Country.query.filter_by(country='Mexico').first()
			self.assertEqual(new_user.languages, [english, spanish])
			self.assertEqual(new_user.countries, [usa, mexico])
			with client.session_transaction() as session:
				self.assertEqual(session[CURR_USER_KEY], new_user.id)
	
	def test_register_username_taken(self):
		with self.client as client:
			response = client.post(
				'/register',
				data={'username': 'testuser', 'password': 'moretesting'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>REGISTER</b></h2>', html)
			self.assertIn('Username &#34;testuser&#34; already exists.', html)
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)
	
	def test_register_invalid_username(self):
		with self.client as client:
			response = client.post(
				'/register',
				data={'username': 'testuser%', 'password': 'moretesting'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>REGISTER</b></h2>', html)
			self.assertIn(
				'Username must only contain letters, numbers, and/or underscores (&#34;_&#34;).',
				html
			)
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)
	
	def test_register_invalid_password(self):
		with self.client as client:
			response = client.post(
				'/register',
				data={'username': 'test_user', 'password': 'blahblah//'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>REGISTER</b></h2>', html)
			self.assertIn(
				'Password must only contain letters, numbers, and/or the following special characters: ! @ $ % &amp; * , . - _',
				html
			)
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)
	
	def test_register_already_logged_in(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/register')
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['Location'], '/top-stories')
	
	def test_logout(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.post('/logout', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn(LOGOUT_MESSAGE.format(username='testuser'), html)
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)
	
	def test_logout_already_logged_out(self):
		with self.client as client:
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)
			response = client.post('/logout', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertNotIn(LOGOUT_MESSAGE.format(username='testuser'), html)
			with client.session_transaction() as session:
				self.assertNotIn(CURR_USER_KEY, session)

class EditUserRoutesTestCase (TestCase):
	"""Test routes related to editing the user and their preferences"""

	def setUp(self):
		with app.app_context():
			Language_Preference.query.delete()
			Locale.query.delete()
			User.query.delete()
			Language.query.delete()
			Country.query.delete()
			db.session.commit()

			user = User.register('testuser', 'usedintesting')
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
	
	def test_get_edit_user_preferences(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get(f'/users/{user.username}/edit')
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Edit User Preferences</title>',
				html
			)
	
	def test_post_edit_user_preferences(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				english = Language.query.filter_by(language='English').first()
				spanish = Language.query.filter_by(english_name='Spanish').first()
				usa = Country.query.filter_by(country='United States Of America').first()
				mexico = Country.query.filter_by(country='Mexico').first()
				self.assertEqual(user.languages, [english, spanish])
				self.assertEqual(user.countries, [usa, mexico])
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.post(
				f'/users/{user.username}/edit',
				data={'languages': ['en'], 'countries': []},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {user.username}</title>',
				html
			)
			self.assertIn(USER_EDIT_SUCCESS_MESSAGE.format(username=user.username), html)
			edited_user = User.query.filter_by(username='testuser').first()
			english_refresh = Language.query.filter_by(language='English').first()
			self.assertEqual(edited_user.languages, [english_refresh])
			self.assertEqual(len(edited_user.countries), 0)
	
	def test_edit_user_preferences_incorrect_user(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/users/anotheruser/edit', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {user.username}</title>',
				html
			)
			self.assertIn(INCORRECT_USER_AUTH_MESSAGE.format(username=user.username), html)
	
	def test_edit_user_preferences_logged_out(self):
		with self.client as client:
			response = client.get('/users/testuser/edit', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn(NEED_TO_LOGIN_AUTH_MESSAGE, html)
	
	def test_get_change_username(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get(f'/users/{user.username}/change-username')
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Username</title>',
				html
			)
	
	def test_post_change_username(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-username',
				data={'username': 'thebestusername', 'password': 'usedintesting'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			edited_user = User.query.filter_by(id=user_id).first()
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {edited_user.username}</title>',
				html
			)
			self.assertIn(USER_EDIT_SUCCESS_MESSAGE.format(username=edited_user.username), html)
			self.assertEqual(edited_user.username, 'thebestusername')
	
	def test_change_username_incorrect_password(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-username',
				data={'username': 'thebestusername', 'password': 'thisiswrong'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Username</title>',
				html
			)
			self.assertIn(INCORRECT_PASSWORD_MESSAGE, html)
			user_refresh = User.query.filter_by(id=user_id).first()
			self.assertEqual(user_refresh.username, 'testuser')
	
	def test_change_username_username_taken(self):
		with self.client as client:
			with app.app_context():
				new_user = User.register('new_user', 'furthertesting')
				db.session.add(new_user)
				db.session.commit()

				new_user_refresh = User.query.filter_by(username='new_user').first()
				self.assertIsInstance(new_user_refresh.id, int)
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-username',
				data={'username': 'new_user', 'password': 'usedintesting'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Username</title>',
				html
			)
			self.assertIn('Username &#34;new_user&#34; already exists.', html)
			user_refresh = User.query.filter_by(id=user_id).first()
			self.assertEqual(user_refresh.username, 'testuser')
	
	def test_change_username_invalid_username(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-username',
				data={'username': 'thebestusername#', 'password': 'usedintesting'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Username</title>',
				html
			)
			self.assertIn(
				'Username must only contain letters, numbers, and/or underscores (&#34;_&#34;).',
				html)
			user_refresh = User.query.filter_by(id=user_id).first()
			self.assertEqual(user_refresh.username, 'testuser')
	
	def test_change_username_incorrect_user(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/users/anotheruser/change-username', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {user.username}</title>',
				html
			)
			self.assertIn(INCORRECT_USER_AUTH_MESSAGE.format(username=user.username), html)
	
	def test_change_username_logged_out(self):
		with self.client as client:
			response = client.get('/users/testuser/change-username', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn(NEED_TO_LOGIN_AUTH_MESSAGE, html)
	
	def test_get_change_password(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get(f'/users/{user.username}/change-password')
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Password</title>',
				html
			)
	
	def test_post_change_password(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-password',
				data={
					'current_password': 'usedintesting',
					'new_password': 'newpassword',
					'confirm_new_password': 'newpassword'
				},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			edited_user = User.query.filter_by(id=user_id).first()
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {edited_user.username}</title>',
				html
			)
			self.assertIn(USER_EDIT_SUCCESS_MESSAGE.format(username=edited_user.username), html)
			self.assertEqual(User.authenticate('testuser', 'newpassword'), edited_user)
			self.assertFalse(User.authenticate('testuser', 'usedintesting'))
	
	def test_change_password_incorrect_password(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-password',
				data={
					'current_password': 'thisiswrong',
					'new_password': 'newpassword',
					'confirm_new_password': 'newpassword'
				},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Password</title>',
				html
			)
			self.assertIn(INCORRECT_PASSWORD_MESSAGE, html)
			user_refresh = User.query.filter_by(id=user_id).first()
			self.assertEqual(User.authenticate('testuser', 'usedintesting'), user_refresh)
			self.assertFalse(User.authenticate('testuser', 'newpassword'))
	
	def test_change_password_nonmatching_new_passwords(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-password',
				data={
					'current_password': 'usedintesting',
					'new_password': 'newpassword',
					'confirm_new_password': 'new_password'
				},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Password</title>',
				html
			)
			self.assertIn(
				'Password entered under &#34;Confirm New Password&#34; does not match &#34;New Password.&#34;',
				html
			)
			user_refresh = User.query.filter_by(id=user_id).first()
			self.assertEqual(User.authenticate('testuser', 'usedintesting'), user_refresh)
			self.assertFalse(User.authenticate('testuser', 'newpassword'))
			self.assertFalse(User.authenticate('testuser', 'new_password'))
	
	def test_change_password_invalid_password(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				user_id = user.id
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user_id
			response = client.post(
				f'/users/{user.username}/change-password',
				data={
					'current_password': 'usedintesting',
					'new_password': 'newpassword^',
					'confirm_new_password': 'newpassword^'
				},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				'<title>News Over Coffee - Change Password</title>',
				html
			)
			self.assertIn(
				'Password must only contain letters, numbers, and/or the following special characters: ! @ $ % &amp; * , . - _',
				html
			)
			user_refresh = User.query.filter_by(id=user_id).first()
			self.assertEqual(User.authenticate('testuser', 'usedintesting'), user_refresh)
			self.assertFalse(User.authenticate('testuser', 'newpassword^'))
	
	def test_change_password_incorrect_user(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/users/anotheruser/change-password', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {user.username}</title>',
				html
			)
			self.assertIn(INCORRECT_USER_AUTH_MESSAGE.format(username=user.username), html)
	
	def test_change_password_logged_out(self):
		with self.client as client:
			response = client.get('/users/testuser/change-password', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn(NEED_TO_LOGIN_AUTH_MESSAGE, html)

class NewsRoutesTestCase (TestCase):
	"""Test routes related to displaying news articles"""

	def setUp(self):
		with app.app_context():
			Language_Preference.query.delete()
			Locale.query.delete()
			User.query.delete()
			Language.query.delete()
			Country.query.delete()
			db.session.commit()

			user = User.register('testuser', 'usedintesting')
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
	
	def test_show_top_stories(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/top-stories')
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			user_refresh = User.query.filter_by(username='testuser').first()
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {user_refresh.username}</title>',
				html
			)
			for country in user_refresh.countries:
				self.assertIn(f'{country.country}', html)
			for language in user_refresh.languages:
				self.assertIn(f'{language.language}', html)
	
	def test_register_then_show_top_stories_with_default_preferences(self):
		with self.client as client:
			response = client.post(
				'/register',
				data={'username': 'secondtestuser', 'password': 'moretesting'},
				follow_redirects=True
			)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			user = User.query.filter_by(username='secondtestuser').first()
			self.assertIn(
				f'<title>News Over Coffee - Top Stories for {user.username}</title>',
				html
			)
			self.assertIn('All - Global News', html)
			self.assertIn('English', html)
	
	def test_show_top_stories_logged_out(self):
		with self.client as client:
			response = client.get('/top-stories', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn(NEED_TO_LOGIN_AUTH_MESSAGE, html)

	def test_search(self):
		with self.client as client:
			with app.app_context():
				user = User.query.filter_by(username='testuser').first()
				with client.session_transaction() as session:
					session[CURR_USER_KEY] = user.id
			response = client.get('/search')
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>SEARCH</b></h2>', html)
			self.assertIn('Keyword:', html)
			self.assertIn('Publication Timeframe:', html)
			self.assertIn('<option value="1">Last 24 Hours</option>', html)
			self.assertIn('<option value="7" selected>Last 7 Days</option>', html)
			self.assertIn('<option value="365">Last Year</option>', html)
	
	def test_search_logged_out(self):
		with self.client as client:
			response = client.get('/search', follow_redirects=True)
			html = response.get_data(as_text=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('<h2 class="mt-3"><b>LOGIN</b></h2>', html)
			self.assertIn(NEED_TO_LOGIN_AUTH_MESSAGE, html)
