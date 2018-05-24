from django.contrib import admin
from . import models


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'positionX', 'positionY', 'level')
	list_editable = ('name', 'positionX', 'positionY', 'level')
	list_filter = ('level', )
	list_per_page = 30


@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
	list_display = ('id', 'positionX', 'positionY', 'station')
	list_select_related = ('station', )
	list_editable = ('positionX', 'positionY')
	list_per_page = 30
	search_fields = ('id', 'station__name')

	class NodeCategory(admin.SimpleListFilter):
		title = 'Node Category'
		parameter_name = 'node_category'

		def lookups(self, request, model_admin):
			return (
				('node', "Node"),
				('station', "Station"),
			)

		def queryset(self, request, queryset):
			if self.value() == 'node':
				return queryset.filter(station__isnull=True)
			if self.value() == 'station':
				return queryset.filter(station__isnull=False)
	list_filter = (NodeCategory, )


@admin.register(models.Segment)
class SegmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'fromNode', 'toNode', 'line', 'length', 'shape')
	list_select_related = ('fromNode', 'toNode', 'line')
	autocomplete_fields = ['fromNode', 'toNode', 'line']


@admin.register(models.Line)
class LineAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'segment_count')
	search_fields = ('name', )

	def segment_count(self, instance):
		return instance.segments.count()
