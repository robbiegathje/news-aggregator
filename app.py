from flask import flash, Flask, g, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegistrationForm
from models import Country, db, Language, User
from secret import SECRET_KEY

CURR_USER_KEY = 'current_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///news'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY

toolbar = DebugToolbarExtension(app)

with app.app_context():
	db.init_app(app)

def do_login(user):
	session[CURR_USER_KEY] = user.id

def do_logout():
	if CURR_USER_KEY in session:
		del session[CURR_USER_KEY]

@app.before_request
def add_logged_in_user_to_g():
	if CURR_USER_KEY in session:
		g.user = User.query.get(session[CURR_USER_KEY])
	else:
		g.user = None

@app.route('/', methods=['GET'])
def properly_redirect():
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
			do_login(user)
			flash(f'Welcome back {user.username}!', 'success')
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
		user = User.register(
			username=form.username.data,
			password=form.password.data
		)
		db.session.add(user)
		db.session.commit()
		if user:
			do_login(user)
			user.add_new_languages(form.languages.data)
			user.add_new_countries(form.countries.data)
			db.session.add(user)
			db.session.commit()
			flash(f'Welcome {user.username}!', 'success')
			return redirect('/top-stories')
	return render_template('users/register.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
	if g.user:
		do_logout()
		flash(f'Logged out {g.user.username}', 'success')
	return redirect('/login')

@app.route('/top-stories', methods=['GET'])
def show_top_stories():
	if not g.user:
		flash('Please login to continue.', 'danger')
		return redirect('/login')
	return render_template('news/top-stories.html')
