from django.db import models
from django.utils import timezone


class Region(models.Model):
    """Model for Region Class."""

    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    class Meta:
        """Override table details."""

        db_table = 'list_region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.name)


class County(models.Model):
    """Model for County Class."""

    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    class Meta:
        """Override table details."""

        db_table = 'list_county'
        verbose_name = 'County'
        verbose_name_plural = 'Counties'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s - %s' % (self.code, self.name)


class Constituency(models.Model):
    """Model for Constituency Class."""

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    class Meta:
        """Override table details."""

        db_table = 'list_constituency'
        verbose_name = 'Constituency'
        verbose_name_plural = 'Constituencies'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s - %s' % (self.code, self.name)


class Ward(models.Model):
    """Model for Ward Class."""

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)

    class Meta:
        """Override table details."""

        db_table = 'list_ward'
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.name)


class PoliticalParty(models.Model):
    """Model for Political Parties Class."""

    code = models.CharField(max_length=3)
    abbrev = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Override table details."""

        db_table = 'list_political_party'
        verbose_name = 'Political Party'
        verbose_name_plural = 'Political Parties'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s : %s' % (self.abbrev, self.name)


class PresidentialCandidate(models.Model):
    """Model for County Level Candidates."""

    candidate_names = models.CharField(max_length=200)
    running_mate_names = models.CharField(max_length=200, null=True)
    party_name = models.CharField(max_length=120, null=True)
    year = models.IntegerField()
    cid = models.IntegerField(default=1)
    party = models.ForeignKey(
        PoliticalParty, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'president_candidates'
        verbose_name = 'Presidential Candidate'
        verbose_name_plural = 'Presidential Candidates'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.candidate_names)


class CountyCandidate(models.Model):
    """Model for County Level Candidates."""

    candidate_names = models.CharField(max_length=200)
    running_mate_names = models.CharField(max_length=200, null=True)
    party_name = models.CharField(max_length=120, null=True)
    position = models.IntegerField()
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.IntegerField()
    party = models.ForeignKey(
        PoliticalParty, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'county_candidates'
        verbose_name = 'County Level Candidate'
        verbose_name_plural = 'County Level Candidates'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.candidate_names)


class ConstituencyCandidate(models.Model):
    """Model for Constituency Level candidates."""

    candidate_names = models.CharField(max_length=200)
    party_name = models.CharField(max_length=120, null=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    year = models.IntegerField()
    party = models.ForeignKey(
        PoliticalParty, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'constituency_candidates'
        verbose_name = 'Constituency Level Candidate'
        verbose_name_plural = 'Constituency Level Candidates'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.candidate_names)


class WardCandidate(models.Model):
    """Model for Constituency Level candidates."""

    candidate_names = models.CharField(max_length=200)
    party_name = models.CharField(max_length=120, null=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    year = models.IntegerField()
    party = models.ForeignKey(
        PoliticalParty, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'ward_candidates'
        verbose_name = 'Ward Level Candidate'
        verbose_name_plural = 'Ward Level Candidates'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.candidate_names)


class RegVoters(models.Model):
    """Model for Ward level registered voters."""

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    reg_voters = models.BigIntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_voters'
        verbose_name = 'Registered Voter'
        verbose_name_plural = 'Registered Voters'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s : %s' % (self.ward, self.reg_voters)


class PCVoters(models.Model):
    """Model for Polling Center voters."""

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    ps_code = models.BigIntegerField()
    ps_name = models.CharField(max_length=200, null=True)
    reg_voters = models.BigIntegerField()
    ps_stations = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'pc_voters'
        verbose_name = 'Polling Center Registered Voter'
        verbose_name_plural = 'Polling Center Registered Voters'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s : %s' % (self.ps_name, self.reg_voters)


class Polls(models.Model):
    """Model for Region Level Polls."""

    asp1 = models.IntegerField(default=0)
    asp2 = models.IntegerField(default=0)
    asp3 = models.IntegerField(default=0)
    asp4 = models.IntegerField(default=0)
    asp5 = models.IntegerField(default=0)
    poll_id = models.IntegerField(default=1)
    region = models.ForeignKey(
        Region, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'polls'
        verbose_name = 'Polls Percentage'
        verbose_name_plural = 'Polls Percentages'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.poll_id)


class RegionCounty(models.Model):
    """Model for Region County Class."""

    region = models.ForeignKey(
        Region, null=True, blank=True, on_delete=models.CASCADE)
    county = models.ForeignKey(
        County, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        """Override table details."""

        db_table = 'list_region_county'
        verbose_name = 'Region County'
        verbose_name_plural = 'Region Counties'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.county)
