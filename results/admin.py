from django.contrib import admin

from geodata.utils import dump_to_csv
from .models import PresidentialResult, Presidential34B


class PresidentialResultAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['name']
    list_display = ['county', 'reg_voters', 'asp1', 'asp2', 'asp3',
                    'asp4', 'valid_votes', 'rej_votes', 'year']
    # readonly_fields = ['area_id']
    list_filter = ['year', 'county']

    actions = [dump_to_csv]


admin.site.register(PresidentialResult, PresidentialResultAdmin)


class Presidential34BAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['name']
    list_display = ['county', 'constituency', 'reg_voters', 'asp1',
                    'asp2', 'asp3', 'asp4', 'valid_votes',
                    'rej_votes', 'year']
    # readonly_fields = ['area_id']
    list_filter = ['year', 'county']

    actions = [dump_to_csv]


admin.site.register(Presidential34B, Presidential34BAdmin)
