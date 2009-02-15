"""
Desired tags:
{% get_changes_for_app [app] [count] as [varname] %}
{% get_changes_for_model [model] [count] as [varname] %}
{% get_changes_for_object [object] [count] as [varname ]%}
"""

from django import template
from django.db.models import get_app
from django.contrib.contenttypes.models import ContentType
from correx.models import Change
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

register = template.Library()

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


class ChangesByAppNode(template.Node):
	def __init__(self, app_label, num, varname):
		self.app_label = app_label
		self.num = int(num)
		self.varname = varname

	def render(self, context):
		try:
			ct_set = ContentType.objects.filter(app_label__icontains=self.app_label)
		except:
			raise template.TemplateSyntaxError (_("app_label %s could not be found") % self.app_label)
		context[self.varname] = \
			Change.objects.filter(is_public=True, content_app=self.app_label).order_by('-pub_date')[:self.num]
		return ''


def do_tags_for_app(parser, token):
	""" 
	Allows a template-level call for the most recent changes for particular app.
	
	Good for sidebars or pulling in a list on a standalone or showcase app.

	Syntax:
	{% get_changes_for_app [app_label] [count] as [varname] %}

	Example usage:
	{% load correx_tags %}
	{% get_changes_for_app newspaper 5 as change_list %}
	{% for change in change_list %}
		<li>{{ change.pub_date}} - {{ change.get_change_type_display }} - {{ change.description }}</li>
	{% endfor %}
	"""
	bits = token.contents.split()
	if len(bits) != 5:
		raise template.TemplateSyntaxError (_("get_latest_changes tag takes exactly five arguments"))
	if bits[3] != 'as':
		raise TemplateSyntaxError(_("fourth argument to %s tag must be 'as'") % bits[0])
	return ChangesByAppNode(bits[1], bits[2], bits[4])


class ChangesBySiteNode(template.Node):
	def __init__(self, id, num, varname):
		self.id = id
		self.num = int(num)
		self.varname = varname

	def render(self, context):
		try:
			site = Site.objects.get(pk=self.id)
		except User.DoesNotExist:
			raise template.TemplateSyntaxError (_("Site id %s could not be found") % self.username)
		context[self.varname] = \
			Change.objects.filter(is_public=True, site=site).order_by('-pub_date')[:self.num]
		return ''


def do_tags_for_site(parser, token):
	""" 
	Allows a template-level call for the most recent changes for particular site.

	Syntax:
	{% get_changes_for_site [site_id] [count] as [varname] %}

	Example usage:
	{% load correx_tags %}
	{% get_changes_for_site 1 5 as change_list %}
	{% for change in change_list %}
		<li>{{ change.pub_date}} - {{ change.get_change_type_display }} - {{ change.description }}</li>
	{% endfor %}
	"""
	bits = token.contents.split()
	if len(bits) != 5:
		raise template.TemplateSyntaxError (_("get_latest_changes tag takes exactly five arguments"))
	if bits[3] != 'as':
		raise TemplateSyntaxError(_("fourth argument to %s tag must be 'as'") % bits[0])
	return ChangesBySiteNode(bits[1], bits[2], bits[4])



class ChangesByUserNode(template.Node):
	def __init__(self, username, num, varname):
		self.username = username
		self.num = int(num)
		self.varname = varname

	def render(self, context):
		try:
			user = User.objects.get(username__iexact=self.username)
		except User.DoesNotExist:
			raise template.TemplateSyntaxError (_("User named %s could not be found") % self.username)
		context[self.varname] = \
			Change.objects.filter(is_public=True, user=user).order_by('-pub_date')[:self.num]
		return ''


def do_tags_for_user(parser, token):
	""" 
	Allows a template-level call for the most recent changes for particular user.
	
	Good for pulling the list into a user profile page.
	
	Syntax:
	{% get_changes_for_user [username] [count] as [varname] %}
	
	Example usage:
	{% load correx_tags %}
	{% get_changes_for_user Otis 5 as change_list %}
	{% for change in change_list %}
		<li>{{ change.pub_date}} - {{ change.get_change_type_display }} - {{ change.description }}</li>
	{% endfor %}
	"""
	bits = token.contents.split()
	if len(bits) != 5:
		raise template.TemplateSyntaxError (_("get_latest_changes tag takes exactly five arguments"))
	if bits[3] != 'as':
		raise TemplateSyntaxError(_("fourth argument to %s tag must be 'as'") % bits[0])
	return ChangesByUserNode(bits[1], bits[2], bits[4])


class LatestChangesNode(template.Node):
	def __init__(self, num, varname):
		self.num = int(num)
		self.varname = varname

	def render(self, context):
		context[self.varname] = Change.objects.live().order_by('-pub_date')[:self.num]
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
		raise template.TemplateSyntaxError (_("get_latest_changes tag takes exactly four arguments"))
	if bits[2] != 'as':
		raise template.TemplateSyntaxError(_("third argument to %s tag must be 'as'") % bits[0])
	return LatestChangesNode(bits[1], bits[3])


register.tag('get_changes_for_app', do_tags_for_app)
register.tag('get_changes_for_site', do_tags_for_site)
register.tag('get_changes_for_user', do_tags_for_user)
register.tag('get_latest_changes', do_latest_changes)