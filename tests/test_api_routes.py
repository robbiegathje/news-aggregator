from constants import API_LANGUAGE_KEY, DATABASE_URL_KEY
from models import db
from unittest import TestCase

import os

os.environ[DATABASE_URL_KEY] = 'postgresql:///test_news'

from app import app

with app.app_context():
	db.init_app(app)
	db.drop_all()
	db.create_all()

class APIRoutesTestCase (TestCase):
	"""Test internal API routes"""

	def setUp(self):
		self.client = app.test_client()

	def test_get_top_stories(self):
		with self.client as client:
			response = client.get('/api/top-stories', query_string={
				API_LANGUAGE_KEY: 'en'
			})

			self.assertTrue(response.json)
			self.assertEqual(response.json['meta']['limit'], 25)
			self.assertEqual(response.json['meta']['page'], 1)
			self.assertEqual(len(response.json['data']), 25)
			for article in response.json['data']:
				self.assertEqual(article[API_LANGUAGE_KEY], 'en')
