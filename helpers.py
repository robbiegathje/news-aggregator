from constants import *
from datetime import datetime, timedelta, timezone
# from secret import API_TOKEN - commented out for production code

import os

API_TOKEN = os.environ.get('API_TOKEN')

def build_api_query(request_args, *keys):
	query_data = {API_TOKEN_KEY: API_TOKEN}
	for key in keys:
		if key == NUM_OF_DAYS_FOR_SEARCH_KEY and NUM_OF_DAYS_FOR_SEARCH_KEY in request_args:
			query_data[API_PUBLISHED_AFTER_DATE_KEY] = (
				datetime.now(timezone.utc) - timedelta(
					int(request_args[NUM_OF_DAYS_FOR_SEARCH_KEY])
					)
			).strftime(API_DATE_STRING_FORMAT)
		else:
			query_data[key] = request_args.get(key, None)
	return query_data
