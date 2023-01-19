from app import app
from models import Country, db, Language, User

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

API_SUPPORTED_LANGUAGES = [
	('ar', 'Arabic', 'عربي'), ('bg', 'Bulgarian', 'български'),
	('bn', 'Bengali'), ('cs', 'Czech', 'čeština'),
	('da', 'Danish', 'dansk'), ('de', 'German', 'Deutsch'),
	('el', 'Greek, Modern', 'Ελληνικά'), ('en', 'English'),
	('es', 'Spanish', 'Español'), ('et', 'Estonian', 'eesti keel'),
	('fa', 'Persian', 'فارسی'), ('fi', 'Finnish', 'Suomalainen'),
	('fr', 'French', 'Français'), ('he', 'Hebrew', 'עִברִית'),
	('hi', 'Hindi', 'हिंदी'), ('hr', 'Croatian', 'Hrvatski'),
	('hu', 'Hungarian', 'Magyar'), ('id', 'Indonesian', 'bahasa Indonesia'),
	('it', 'Italian', 'Italiano'), ('ja', 'Japanese', '日本語'),
	('ko', 'Korean', '한국인'), ('lt', 'Lithuanian', 'lietuvių'),
	('multi'), ('nl', 'Dutch', 'Nederlands'),
	('no', 'Norwegian', 'norsk'), ('pl', 'Polish', 'Polski'),
	('pt', 'Portuguese', 'Português'), ('ro', 'Romanian', 'Română'),
	('ru', 'Russian', 'Русский'), ('sk', 'Slovak', 'slovenský'),
	('sv', 'Swedish', 'svenska'), ('ta', 'Tamil', 'தமிழ்'),
	('th', 'Thai', 'แบบไทย'), ('tr', 'Turkish', 'Türk'),
	('uk', 'Ukrainian', 'українська'), ('vi', 'Vietnamese', 'Tiếng Việt'),
	('zh', 'Chinese', '中国人')
]
