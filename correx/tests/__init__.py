from django.contrib.auth.models import User
from correx.models import Change
from correx.tests.models import Article, Author
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase
from django.db.models.loading import get_apps, load_app

from django.conf import settings
old_installed_apps = settings.INSTALLED_APPS
model_label = 'correx.tests'
mod = load_app(model_label)
settings.INSTALLED_APPS.append(model_label)

#Shortut
CT = ContentType.objects.get_for_model

# Helper base class for changes tests that need data.
class ChangeTestCase(TestCase):
    fixtures = ["correx_tests"]
    
    def createSomeChanges(self):
        # A change without links to objects
        change_without_link = Change.objects.create(
            description='Correction without connection', 
            change_type=1, 
            pub_date='2009-02-14',
            is_public=True
        )
        # A change with a site
        lat_data_desk = Site.objects.create(
            domain='projects.latimes.com', 
            name='Los Angeles Times Data Desk'
        )
        change_with_site = Change.objects.create(
            description='Site-level addition', 
            change_type=3, 
            pub_date='2009-02-14', 
            site=lat_data_desk,
            is_public=True
        )
        # A change with a user
        russ = User.objects.create(
            username='Russ', 
            first_name='Russ', 
            last_name='Stanton', 
            email='russ@latimes.com', 
            password='34ea4aaaf24efcbb4b30d27302f8657f', 
            is_staff=True, 
            is_active=True,
            is_superuser=True
        )
        change_with_user = Change.objects.create(
            description='Russ makes a site-wide addition', 
            change_type=3, 
            pub_date='2009-02-14', 
            site=lat_data_desk, 
            user=russ,
            is_public=True
        )
        # A change with an app
        author_ct = CT(Author)
        change_with_app = Change.objects.create(
            description='An app-wide update', 
            change_type=2, 
            pub_date='2009-02-15', 
            site=lat_data_desk, 
            user=russ, 
            content_app=author_ct.app_label,
            is_public=True
        )
        # A change with a model
        change_with_model = Change.objects.create(
            description='An update to an author bio', 
            change_type=2, 
            pub_date='2009-02-14', 
            site=lat_data_desk, 
            user=russ, 
            content_app=author_ct.app_label, 
            content_type=author_ct,
            is_public=True
        )
        # A change with an object
        article_ct = CT(Article)
        change_with_object = Change.objects.create(
            description='A correction to a story', 
            change_type=1, 
            pub_date='2009-02-16', 
            site=lat_data_desk, 
            user=russ, 
            content_app=article_ct.app_label, 
            content_type=article_ct,
            object_id = 1,
            is_public=True
        )

        return change_without_link, change_with_site, change_with_user, change_with_app, change_with_model, change_with_object

from correx.tests.unittests.model_tests import *
from correx.tests.unittests.templatetag_tests import *
settings.INSTALLED_APPS = old_installed_apps