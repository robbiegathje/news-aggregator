from app import app
from models import Country, db, Language, User

# List of countries supported by the API as of January 19, 2023 in format:
# 	(2-character-code, country in English)
API_SUPPORTED_COUNTRIES = [
	('ar', 'Argentina'), ('am', 'Armenia'), ('au', 'Australia'),
	('at', 'Austria'), ('by', 'Belarus'), ('be', 'Belgium'),
	('bo', 'Bolivia'), ('br', 'Brazil'), ('bg', 'Bulgaria'),
	('ca', 'Canada'), ('cl', 'Chile'), ('cn', 'China'),
	('co', 'Colombia'), ('hr', 'Croatia'), ('cz', 'Czechia'),
	('ec', 'Ecuador'), ('eg', 'Egypt'), ('fr', 'France'),
	('de', 'Germany'), ('gr', 'Greece'), ('hn', 'Honduras'),
	('hk', 'Hong Kong'), ('in', 'India'), ('id', 'Indonesia'),
	('ir', 'Iran'), ('ie', 'Ireland'), ('il', 'Israel'),
	('it', 'Italy'), ('jp', 'Japan'), ('kr', 'Korea'),
	('mx', 'Mexico'), ('nl', 'Netherlands'), ('nz', 'New Zealand'),
	('ni', 'Nicaragua'), ('pk', 'Pakistan'), ('pa', 'Panama'),
	('pe', 'Peru'), ('pl', 'Poland'), ('pt', 'Portugal'),
	('qa', 'Qatar'), ('ro', 'Romania'), ('ru', 'Russia'),
	('sa', 'Saudi Arabia'), ('za', 'South Africa'), ('es', 'Spain'),
	('ch', 'Switzerland'), ('sy', 'Syria'), ('tw', 'Taiwan'),
	('th', 'Thailand'), ('tr', 'Turkey'), ('ua', 'Ukraine'),
	('gb', 'United Kingdom'), ('us', 'United States Of America'),
	('uy', 'Uruguay'), ('ve', 'Venezuela')
]

# List of languages supported by the API as of January 19, 2023 in format:
# 	(2-character-code, English name, language)
API_SUPPORTED_LANGUAGES = [
	('ar', 'Arabic', 'عربي'), ('bg', 'Bulgarian', 'български'),
	('bn', 'Bengali', 'বাংলা'), ('cs', 'Czech', 'čeština'),
	('da', 'Danish', 'dansk'), ('de', 'German', 'Deutsch'),
	('el', 'Greek', 'Ελληνικά'), ('en', 'English', 'English'),
	('es', 'Spanish', 'Español'), ('et', 'Estonian', 'eesti keel'),
	('fa', 'Persian', 'فارسی'), ('fi', 'Finnish', 'Suomalainen'),
	('fr', 'French', 'Français'), ('he', 'Hebrew', 'עִברִית'),
	('hi', 'Hindi', 'हिंदी'), ('hr', 'Croatian', 'Hrvatski'),
	('hu', 'Hungarian', 'Magyar'), ('id', 'Indonesian', 'bahasa Indonesia'),
	('it', 'Italian', 'Italiano'), ('ja', 'Japanese', '日本語'),
	('ko', 'Korean', '한국인'), ('lt', 'Lithuanian', 'lietuvių'),
	('nl', 'Dutch', 'Nederlands'), ('no', 'Norwegian', 'norsk'),
	('pl', 'Polish', 'Polski'), ('pt', 'Portuguese', 'Português'),
	('ro', 'Romanian', 'Română'), ('ru', 'Russian', 'Русский'),
	('sk', 'Slovak', 'slovenský'), ('sv', 'Swedish', 'svenska'),
	('ta', 'Tamil', 'தமிழ்'), ('th', 'Thai', 'แบบไทย'),
	('tr', 'Turkish', 'Türk'), ('uk', 'Ukrainian', 'українська'),
	('vi', 'Vietnamese', 'Tiếng Việt'), ('zh', 'Chinese', '中国人')
]

with app.app_context():
	db.init_app(app)

	for country in API_SUPPORTED_COUNTRIES:
		new_country = Country(code=country[0], country=country[1])
		db.session.add(new_country)
	
	for lang in API_SUPPORTED_LANGUAGES:
		new_lang = Language(
			code=lang[0],
			english_name=lang[1],
			language=lang[2]
		)
		db.session.add(new_lang)
	
	db.session.commit()
