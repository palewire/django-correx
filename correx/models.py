from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from correx.managers import ChangeLogManager

import datetime


class ChangeLog(models.Model):
	"""
	A change or correction related another app, model or object.
	
	>>> correction_with_no_links = ChangeLog.objects.create(description='Hello Los Angeles', change_type=1, pub_date='1982-07-22')
	>>> correction_with_no_links
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	>>> update_with_no_links = ChangeLog.objects.create(description='Hello Los Angeles', change_type=2, pub_date='1982-07-22')
	>>> update_with_no_links
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	>>> addition_with_no_links = ChangeLog.objects.create(description='Hello Los Angeles', change_type=3, pub_date='1982-07-22')
	>>> addition_with_no_links
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	>>> deletion_with_no_links = ChangeLog.objects.create(description='Hello Los Angeles', change_type=4, pub_date='1982-07-22')
	>>> deletion_with_no_links
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	
	>>> lat_data_desk = Site(domain='projects.latimes.com', name='Los Angeles Times Data Desk')
	>>> change_with_site = ChangeLog.objects.create(description='Hello Los Angeles', change_type=3, pub_date='1982-07-22', site=lat_data_desk)
	>>> change_with_site
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	
	>>> otis = User(username='Otis', first_name='Otis', last_name='Chandler', email='otis@latimes.com', password='latimes', is_staff=True, is_superuser=True)
	>>> change_with_user = ChangeLog.objects.create(description='Hello Los Angeles', change_type=3, pub_date='1982-07-22', site=lat_data_desk, user=otis)
	>>> change_with_user
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	
	>>> mapping_la = 'mapping_la'
	>>> change_with_app = ChangeLog.objects.create(description='Hello Los Angeles', change_type=3, pub_date='1982-07-22', site=lat_data_desk, user=otis, content_app=mapping_la)
	>>> change_with_app
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	
	>>> neighborhood = ContentType(name='Neighborhood', app_label='mapping_la', model='neighborhood')
	>>> change_with_model = ChangeLog.objects.create(description='Hello Los Angeles', change_type=3, pub_date='1982-07-22', site=lat_data_desk, user=otis, content_app=mapping_la, content_type=neighborhood)
	>>> change_with_model
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	
	>>> neighborhood_pk = 1
	>>> change_with_object = ChangeLog.objects.create(description='Hello Los Angeles', change_type=3, pub_date='1982-07-22', site=lat_data_desk, user=otis, content_app=mapping_la, content_type=neighborhood, object_id=neighborhood_pk)
	>>> change_with_object
	<ChangeLog: 1982-07-22: Hello Los Angeles...>
	
	"""
	# The different type of changes available. 
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
	objects = ChangeLogManager()
	
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
