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
			'random': 'crazy'}
		query = build_api_query(
			request_args,
			API_LANGUAGE_KEY,
			API_LOCALE_KEY)

		self.assertEqual(query[API_TOKEN_KEY], API_TOKEN)
		self.assertEqual(query[API_LANGUAGE_KEY], 'en')
		self.assertEqual(query[API_LOCALE_KEY], 'us')
		self.assertNotIn('random', query)
