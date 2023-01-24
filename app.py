from flask import flash, Flask, g, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegistrationForm
from models import Country, db, Language, User
from secret import API_TOKEN, SECRET_KEY

import requests

API_BASE_URL = 'https://api.thenewsapi.com/v1/news'
CURR_USER_KEY = 'current_user'
FLASH_DANGER_CATEGORY = 'danger'
FLASH_SUCCESS_CATEGORY = 'success'
LOGOUT_MESSAGE = 'Successfully logged out {username}.'
NEED_TO_LOGIN_AUTH_MESSAGE = 'Please login to continue.'
WELCOME_NEW_USER_MESSAGE = 'Welcome {username}!'
WELCOME_RETURNING_USER_MESSAGE = 'Welcome back {username}!'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///news'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY

toolbar = DebugToolbarExtension(app)

with app.app_context():
	db.init_app(app)

def add_user_id_to_session(user):
	session[CURR_USER_KEY] = user.id

def remove_user_id_from_session():
	if CURR_USER_KEY in session:
		del session[CURR_USER_KEY]

@app.before_request
def add_logged_in_user_to_g():
	if CURR_USER_KEY in session:
		g.user = User.query.get(session[CURR_USER_KEY])
	else:
		g.user = None

@app.route('/', methods=['GET'])
def show_home_experience():
	"""
	If user is logged in, user is immediately redirected to the
	top stories page, which acts as the site's homepage.
	However, user is redirected to the login page when they are not logged in.
	Thus, the 'home experience' is different for logged in user
	than logged out user.
	"""
	if g.user:
		return redirect('/top-stories')
	return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.login(
			username=form.username.data,
			password=form.password.data
		)
		if user:
			add_user_id_to_session(user)
			flash(
				WELCOME_RETURNING_USER_MESSAGE.format(username=user.username),
				FLASH_SUCCESS_CATEGORY
			)
			return redirect('/top-stories')
	return render_template('users/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	form.languages.choices = [
		(lang.code, lang.language) for lang in Language.query.all()
	]
	form.countries.choices = [
		(country.code, country.country) for country in Country.query.all()
	]
	if form.validate_on_submit():
		# needs refactor
		user = User.register(
			username=form.username.data,
			password=form.password.data
		)
		db.session.add(user)
		db.session.commit()
		if user:
			add_user_id_to_session(user)
			user.add_new_languages(form.languages.data)
			user.add_new_countries(form.countries.data)
			db.session.add(user)
			db.session.commit()
			flash(
				WELCOME_NEW_USER_MESSAGE.format(username=user.username),
				FLASH_SUCCESS_CATEGORY
			)
			return redirect('/top-stories')
	return render_template('users/register.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
	if g.user:
		remove_user_id_from_session()
		flash(
			LOGOUT_MESSAGE.format(username=g.user.username),
			FLASH_SUCCESS_CATEGORY
		)
	return redirect('/login')

@app.route('/top-stories', methods=['GET'])
def show_top_stories():
	if not g.user:
		flash(NEED_TO_LOGIN_AUTH_MESSAGE, FLASH_DANGER_CATEGORY)
		return redirect('/login')
	return render_template('news/top-stories.html')


# API
@app.route('/api/top-stories')
def get_top_stories():
	query_data = {
		'api_token': API_TOKEN,
		'language': request.args['language'],
		'locale': request.args['locale'] if 'locale' in request.args else None,
		'page': request.args['page'] if 'page' in request.args else 1
	}
	news_api_response = requests.get(f'{API_BASE_URL}/top', params=query_data)
	return news_api_response.json()

@app.route('/api/all-stories')
def get_all_stories():
	query_data = {
		'api_token': API_TOKEN,
		'language': request.args['language'],
		'page': request.args['page'] if 'page' in request.args else 1
	}
	news_api_response = requests.get(f'{API_BASE_URL}/all', params=query_data)
	return news_api_response.json()

@app.route('/api/search')
def get_stories_by_search_term():
	query_data = {
		'api_token': API_TOKEN,
		'search': request.args['search'] if 'search' in request.args else None,
		'language': request.args['language'],
		'locale': request.args['locale'] if 'locale' in request.args else None,
		'page': request.args['page'] if 'page' in request.args else 1,
		# 'published_after': 'today - x number of days' (IMPLEMENT THIS)
	}
	news_api_response = requests.get(f'{API_BASE_URL}/top', params=query_data)
	return news_api_response.json()
