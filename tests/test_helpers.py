from constants import *
from helpers import build_api_query
from secret import API_TOKEN
from unittest import TestCase

class HelperFunctionsTestCase (TestCase):
	"""Test helper functions for News Aggregator App"""

	def test_build_api_query(self):
		request_args = {
			API_LANGUAGE_KEY: 'en',
			API_LOCALE_KEY: 'us',
			'random': 'crazy'
		}
		query = build_api_query(
			request_args,
			API_LANGUAGE_KEY,
			API_LOCALE_KEY,
			NUM_OF_DAYS_FOR_SEARCH_KEY
		)

		self.assertEqual(query[API_TOKEN_KEY], API_TOKEN)
		self.assertEqual(query[API_LANGUAGE_KEY], 'en')
		self.assertEqual(query[API_LOCALE_KEY], 'us')
		self.assertNotIn('random', query)
		self.assertIsNone(query[NUM_OF_DAYS_FOR_SEARCH_KEY])
	
	def test_build_api_query_with_search_days(self):
		request_args = {
			API_LANGUAGE_KEY: 'en',
			API_LOCALE_KEY: 'us',
			NUM_OF_DAYS_FOR_SEARCH_KEY: '7'
		}
		query = build_api_query(
			request_args,
			API_LANGUAGE_KEY,
			API_LOCALE_KEY,
			NUM_OF_DAYS_FOR_SEARCH_KEY
		)

		self.assertEqual(query[API_TOKEN_KEY], API_TOKEN)
		self.assertEqual(query[API_LANGUAGE_KEY], 'en')
		self.assertEqual(query[API_LOCALE_KEY], 'us')
		self.assertIn(API_PUBLISHED_AFTER_DATE_KEY, query)
		self.assertNotIn(NUM_OF_DAYS_FOR_SEARCH_KEY, query)
