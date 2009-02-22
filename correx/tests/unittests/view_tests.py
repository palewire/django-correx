from django.test.client import Client

from correx.tests import ChangeTestCase
from correx.models import Change, ChangeType


class CorrexViewTests(ChangeTestCase):
	
	def setUp(self):
	"""
	Setting up the test client for reuse throughout.
	"""
		self.client = Client()
		self.app_list = [i[0] for i in Change().APP_CHOICES]

	def testFilterContentTypesByApp(self):
		"""
		Test the admin jQuery's request for the list of models 
		associated with a particular application.
		"""
		url = '/correx/admin/filter/contenttype/'
		
		for app in self.app_list:
			# Issue a GET request.
			response = self.client.get(url, {'app_label': app})
			# Check that the response is 200 OK.
			self.failUnlessEqual(response.status_code, 200)
			print response.content
