from django.utils import simplejson
from django.template import RequestContext
from django.http import Http404, HttpResponse

from django.contrib.contenttypes.models import ContentType

def filter_contenttypes_by_app(request):
	""" 
	Intended to fetch AJAX calls from admin templates.
	"""
	# If there is not a POST request throw a 404
	if not request.GET:
		raise Http404
		
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
