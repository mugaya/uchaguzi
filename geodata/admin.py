from django.contrib import admin
from .models import WardMaps
from .utils import dump_to_csv


'''
class WardMapsAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['name']
    list_display = ['gid', 'uid', 'county', 'subcounty',
                    'ward', 'scuid', 'cuid']
    # readonly_fields = ['area_id']
    list_filter = ['county']

    actions = [dump_to_csv]


admin.site.register(WardMaps, WardMapsAdmin)
'''


admin.site.register(WardMaps, admin.ModelAdmin)