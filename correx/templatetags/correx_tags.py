"""
Desired tags:
{% get_recent_changes [count] as [varname] %}
{% get_changes_for_user [user] [count] as [varname] %}
{% get_changes_for_site [site] [count] as [varname] %}
{% get_changes_for_app [app] [count] as [varname] %}
{% get_changes_for_model [model] [count] as [varname] %}
{% get_changes_for_object [object] [count] as [varname ]%}
"""


from django import template
from django.db.models import get_app
from django.contrib.contenttypes.models import ContentType
from correx.models import Change
from django.utils.translation import ugettext_lazy as _

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
	Allows a template-level call for the most recent changes regardless of user, site, app, model or object.
	
	Good for pulling the list into sidebars that run across an app or site.
	
	Syntax:
	{% get_latest_changes [count] as [varname] %}
	
	Example usage:
	{% load correx_tags %}
	{% get_latest_changes 5 as latest_changes %}
	{% for change in latest_changes %}
		<li>{{ change.pub_date}} - {{ change.get_change_type_display }} - {{ change.description }}</li>
	{% endfor %}
	"""
	
	bits = token.contents.split()
	if len(bits) != 4:
		raise template.TemplateSyntaxError ("'get_latest_changes tag takes exactly three arguments")
	if bits[2] != 'as':
		raise template.TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
	return LatestChangesNode(bits[1], bits[3])


class LatestChangesNode(template.Node):
	def __init__(self, num, varname):
		self.num = int(num)
		self.varname = varname

	def render(self, context):
		context[self.varname] = Change.objects.live().order_by('-pub_date')[:self.num]
		return ''


register = template.Library()
register.tag('get_changes_for_object', do_changes_by_object)
register.tag('get_latest_changes', do_latest_changes)