from django import template
from django.db.models import get_app
from django.contrib.contenttypes.models import ContentType
from correx.models import Change

def do_changes_by_object(parser, token):
	""" 
	Allows a template-level call for the changes for a particular object.
	
	Good for pulling the list into object_detail pages.
	
	Syntax:
	{% get_changes_for_object [object] %}
	
	Example usage:
	{% load correx_tags %}
	{% get_changes_for_object object %}
	{% for change in change_list %}
		<li>{{ change.pub_date }} - {{ change.get_change_type_display }} - {{ change.description }}</li>
	{% endfor %}
	"""
	bits = token.contents.split()
	if len(bits) != 2:
		raise template.TemplateSyntaxError ("get_latest_changes tag takes exactly two arguments")
	obj_arg = bits[1]
	return ChangesByObjectNode(obj_arg)


class ChangesByObjectNode(template.Node):
	def __init__(self, obj):
		self.obj = template.Variable(obj)

	def render(self, context):
		resolved_obj = self.obj.resolve(context)
		try:
			ctype = ContentType.objects.get_for_model(resolved_obj)
		except:
			raise template.TemplateSyntaxError ("model could not be found for object")
		context['change_list'] = \
			Change.objects.filter(is_public=True, content_type=ctype.pk, object_id=resolved_obj.pk).order_by('-pub_date')
		return ''


def do_latest_changes(parser, token):
	""" 
	Allows a template-level call for the most recent changes for a particular app, or all apps.
	
	Good for pulling the list into sidebars that run across an app or site.
	
	Syntax:
	{% get_latest_changes [app] [count] %}
	
	Example usage:
	{% load correx_tags %}
	{% get_latest_changes all_apps 5 %}
	{% for change in latest_changes %}
		<li>{{ change.pub_date}} - {{ change.get_change_type_display }} - {{ change.description }}</li>
	{% endfor %}
	"""
	
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError ("'get_latest_changes tag takes exactly three arguments")
	app_arg = bits[1]
	if app_arg == 'all_apps':
		return LatestChangesFromAllAppsNode(bits[2])
	else:
		app = get_app(app_arg)
		if app is None:
			raise template.TemplateSyntaxError("'get_latest_changes' tag got an invalid app name: %s" % bits[1])
		return LatestChangesNode(app_arg, bits[2])


class LatestChangesFromAllAppsNode(template.Node):
	def __init__(self, num):
		self.num = int(num)

	def render(self, context):
		context['latest_changes'] = \
			Change.objects.live().order_by('-pub_date')[:self.num]
		return ''


class LatestChangesNode(template.Node):
	def __init__(self, app, num):
		self.app = app
		self.num = int(num)

	def render(self, context):
		context['latest_changes'] = \
			Change.objects.filter(is_public=True, content_app=self.app).order_by('-pub_date')[:self.num]
		return ''


register = template.Library()
register.tag('get_changes_for_object', do_changes_by_object)
register.tag('get_latest_changes', do_latest_changes)