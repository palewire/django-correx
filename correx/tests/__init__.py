from django.contrib.auth.models import User
from correx.models import Change
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase
from correx.tests.models import Article, Author

# Helper base class for changes tests that need data.
class ChangeTestCase(TestCase):
    fixtures = ["tests"]
    
    def createSomeChanges(self):
        # A change without links to objects
        change_without_link = Change.objects.create(
            description='Correction without connection', 
            change_type=1, 
            pub_date='2009-02-14'
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
            site=lat_data_desk
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
            user=russ
        )
        # A change with an app
        author = ContentType.objects.create(
            name='Author', 
            app_label='newspaper.com', 
            model='author'
        )
        change_with_app = Change.objects.create(
            description='An app-wide update', 
            change_type=2, 
            pub_date='2009-02-14', 
            site=lat_data_desk, 
            user=russ, 
            content_app=author.app_label
        )
        # A change with a model
        change_with_model = Change.objects.create(
            description='An update to an author bio', 
            change_type=2, 
            pub_date='2009-02-14', 
            site=lat_data_desk, 
            user=russ, 
            content_app=author.app_label, 
            content_type=author
        )
        # A change with an object
        article = ContentType.objects.create(
            name='Article', 
            app_label='newspaper.com', 
            model='article'
        )
        change_with_object = Change.objects.create(
            description='A correction to a story', 
            change_type=1, 
            pub_date='2009-02-14', 
            site=lat_data_desk, 
            user=russ, 
            content_app=article.app_label, 
            content_type=article,
            object_id = 1
        )

        return change_without_link, change_with_site, change_with_user, change_with_app, change_with_model, change_with_object

from correx.tests.model_tests import *