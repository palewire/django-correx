from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from correx.managers import ChangeManager

import datetime


class Change(models.Model):
	"""
	A change that is optionally related to a site, app, model or object.
	"""
	# The different types of changes available. 
	# This could potentially be broken out into its own model 
	# so that new types could be added in the admin panel.
	CHANGE_TYPES = (
		(1, 'Correction'),
		(2, 'Update'),
		(3, 'Addition'),
		(4, 'Deletion'),
	)
	
	# A list of all the installed apps in a set of paired tuples.
	# I've excluded the django contrib apps and included them as
	# strings to avoid "magic numbers" and so that it won't matter 
	# if you change their order in settings.py
	installed_apps = [(i, i) for i in settings.INSTALLED_APPS if i.find('django')]
	installed_apps.sort()
	APP_CHOICES = installed_apps
	
	# The change
	description    = models.TextField(help_text=_('A description of the change'))
	change_type    = models.IntegerField(choices=CHANGE_TYPES, help_text=_('The type of change'))
	pub_date       = models.DateTimeField(default=datetime.datetime.now)
	is_public      = models.BooleanField(default=False, help_text=_('Check this box to publish the comment on the live site.'), verbose_name=_('Publish'))

	# Optional connection to the user making the change
	user           = models.ForeignKey(User, blank=True, null=True, related_name="%(class)s_comments", help_text=_('The name of the user responsible for the change. Optional.'))

	# Optional connections to sites, apps, models and objects in the database
	site           = models.ForeignKey(Site, null=True, blank=True, help_text=_('The site being changed. Optional.'))
	content_app    = models.CharField(max_length=200, choices=APP_CHOICES, null=True, blank=True, help_text=_('The application being changed. Optional.'), verbose_name=_('App'))
	content_type   = models.ForeignKey(ContentType, null=True, blank=True, related_name="content_type_set_for_%(class)s", help_text=_('The table or model being changed. Optional.'), verbose_name=_('Model'))
	object_id      = models.PositiveIntegerField(null=True, blank=True, help_text=_('The particular database record being changed. Optional.'))
	content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')
	
	# Managers
	objects = ChangeManager()
	
	class Meta:
		db_table = 'django_content_changelog'
		ordering = ['-pub_date']
		get_latest_by = "pub_date"
		verbose_name = 'change'

	def __unicode__(self):
		return u'%s: %s...' % (self.pub_date, self.description[:50])
		
	def get_content_object(self):
		from django.core.exceptions import ObjectDoesNotExist
		try:
			return self.content_object
		except ObjectDoesNotExist:
			return None

	get_content_object.short_description = _('Record')
