from django.contrib import admin
from .models import (
    County, PoliticalParty, CountyCandidate, ConstituencyCandidate,
    Constituency, Ward, PresidentialCandidate, Polls, Region,
    RegionCounty, WardCandidate, PCVoters)
from geodata.utils import dump_to_csv


@admin.register(
    County, Constituency, Ward, Region, PCVoters,
    PresidentialCandidate, RegionCounty)
class PersonAdmin(admin.ModelAdmin):
    actions = [dump_to_csv]
    pass


class PollsAdmin(admin.ModelAdmin):
    """Admin back end Polls."""

    search_fields = ['region__name']
    list_display = ['poll_id', 'region', 'asp1', 'asp2', 'asp3', 'asp4']
    # readonly_fields = ['area_id']
    list_filter = ['region__name', 'poll_id']
    actions = [dump_to_csv]


admin.site.register(Polls, PollsAdmin)


class PoliticalPartyAdmin(admin.ModelAdmin):
    """Admin back end Polls."""

    search_fields = ['code', 'abbrev', 'name']
    list_display = ['id', 'code', 'abbrev', 'name']
    # readonly_fields = ['area_id']
    list_filter = []
    actions = [dump_to_csv]


admin.site.register(PoliticalParty, PoliticalPartyAdmin)


class CountyCandidateAdmin(admin.ModelAdmin):
    """Admin back end Polls."""

    search_fields = ['candidate_names', 'running_mate_names']
    list_display = ['id', 'county_id', 'county', 'position',
                    'candidate_names', 'running_mate_names',
                    'year']
    # readonly_fields = ['area_id']
    list_filter = ['year', 'position', 'county']
    actions = [dump_to_csv]


admin.site.register(CountyCandidate, CountyCandidateAdmin)


class ConstituencyCandidateAdmin(admin.ModelAdmin):
    """Admin back end Polls."""

    search_fields = ['candidate_names', 'party_name',
                     'constituency__code', 'constituency__name']
    list_display = ['id', 'constituency_id', 'constituency', 'candidate_names',
                    'party', 'year']
    # readonly_fields = ['area_id']
    list_filter = ['year', 'constituency']
    actions = [dump_to_csv]


admin.site.register(ConstituencyCandidate, ConstituencyCandidateAdmin)


class WardCandidateAdmin(admin.ModelAdmin):
    """Admin back end Polls."""

    search_fields = ['candidate_names', 'party_name',
                     'ward__code', 'ward__name']
    list_display = ['id', 'county', 'constituency', 'ward_id', 'ward',
                    'candidate_names', 'party', 'year']
    # readonly_fields = ['area_id']
    list_filter = ['year', 'constituency']
    actions = [dump_to_csv]


admin.site.register(WardCandidate, WardCandidateAdmin)
