from django.db import models
from django.dispatch import dispatcher

class ChangeManager(models.Manager):

	def live(self):
		"""
		QuerySet for all changes set for publication.
		"""
		return self.get_query_set().filter(is_public=True)
