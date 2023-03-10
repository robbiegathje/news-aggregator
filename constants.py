"""
Constants for News Aggregator App
All references to 'API' are references to
The News API at https://www.thenewsapi.com/
"""

# Constants related to The News API
API_BASE_URL = 'https://api.thenewsapi.com/v1/news'
API_DATE_STRING_FORMAT = '%Y-%m-%d'
API_LANGUAGE_KEY = 'language'
API_LOCALE_KEY = 'locale'
API_PAGE_NUMBER_KEY = 'page'
API_PUBLISHED_AFTER_DATE_KEY = 'published_after'
API_SEARCH_TERM_KEY = 'search'
API_TOKEN_KEY = 'api_token'
NUM_OF_DAYS_FOR_SEARCH_KEY = 'days'


# Constants related to user status and messaging
CURR_USER_KEY = 'current_user'
FLASH_DANGER_CATEGORY = 'danger'
FLASH_SUCCESS_CATEGORY = 'success'
INCORRECT_USER_AUTH_MESSAGE = 'Unauthorized. Currently logged in as {username}.'
INCORRECT_PASSWORD_MESSAGE = 'Incorrect password.'
INVALID_USERNAME_MESSAGE = 'Username must only contain letters, numbers, and/or underscores ("_").'
INVALID_PASSWORD_MESSAGE = 'Password must only contain letters, numbers, and/or the following special characters: ! @ $ % & * , . - _'
LOGOUT_MESSAGE = 'Successfully logged out {username}.'
NEED_TO_LOGIN_AUTH_MESSAGE = 'Please login to continue.'
NEW_PASSWORD_MATCHES_OLD_MESSAGE = 'Your new password cannot be the same as your current password.'
UNCONFIRMED_NEW_PASSWORD_MESSAGE = 'Password entered under "Confirm New Password" does not match "New Password."'
USERNAME_ALREADY_EXISTS_MESSAGE = 'Username "{username}" already exists.'
USERNAME_DOES_NOT_EXIST_MESSAGE = 'Username "{username}" does not exist.'
USER_EDIT_SUCCESS_MESSAGE = 'Successfully edited {username}.'
WELCOME_NEW_USER_MESSAGE = 'Welcome {username}!'
WELCOME_RETURNING_USER_MESSAGE = 'Welcome back {username}!'

# Constants related to username & password validation
PASSWORD_REGEXP = '^[\w!@$%&*,.-]+$'
USERNAME_REGEXP = '^\w+$'
