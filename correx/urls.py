from django.conf.urls.defaults import *

urlpatterns = patterns('correx.views',
  (r'^admin/filter/contenttype/$', 'filter_contenttypes_by_app'),
)