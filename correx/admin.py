from django.contrib import admin
from correx.models import ChangeLog

class ChangeLogAdmin(admin.ModelAdmin):
	list_display = ('pub_date', 'change_type', 'description', 'user', 'site', 'content_app', 'content_type', 'get_content_object',)
	search_fields = ['description', 'user', 'site', 'content_type', 'content_type', 'change_type']
	list_filter = ('change_type', 'site', 'content_app')
	date_hierarchy = 'pub_date'
	fieldsets = (
		('Editorial', { 'fields': ('pub_date', 'change_type', 'description',)}),
		('Meta', { 'fields': ('user', 'site', 'content_app', 'content_type', 'object_id',)}),
		('Publishing', { 'fields': ('is_public',)}),
	)

admin.site.register(ChangeLog, ChangeLogAdmin)