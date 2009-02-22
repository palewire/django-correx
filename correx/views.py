from django.utils import simplejson
from django.template import RequestContext
from django.http import Http404, HttpResponse

from django.contrib.contenttypes.models import ContentType

def filter_contenttypes_by_app(request):
	""" 
	Accepts an app_label as a query_string and returns its associated model set 
	as JSON in a format designed to fill an in an HTML dropdown menu.
	
	HTTP GET is required.
	"""
	# If there is not a GET request throw a 404
	if not request.GET:
		raise Http404
	
	# Seed the response JSON with the bare minimum, enough to fill an empty select box
	response_list = [{'Text': '---------', 'Value': ''}]
	
	# Grab the post variable
	qs = request.GET.get('app_label')
	if not qs:
		HttpResponse(simplejson.dumps(response_list), mimetype='application/javascript')
	
	try:
		# Fetch all of the ContentType records from that app
		content_types = ContentType.objects.filter(app_label=qs)
	except:
		raise Http404
	
	# Load the results into the dictionary
	for ct in content_types:
		response_list += [{'Text': ct.model, 'Value': str(ct.pk)}]

	return HttpResponse(simplejson.dumps(response_list), mimetype='application/javascript')
