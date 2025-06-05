from django.db import models
from django.utils import timezone

from candidates.models import County, Constituency


class PresidentialResult(models.Model):
    """Model for Polling Center voters."""

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    reg_voters = models.BigIntegerField(default=0)
    asp1 = models.BigIntegerField(default=0)
    asp2 = models.BigIntegerField(default=0)
    asp3 = models.BigIntegerField(default=0)
    asp4 = models.BigIntegerField(default=0)
    asp5 = models.BigIntegerField(default=0)
    asp6 = models.BigIntegerField(default=0)
    asp7 = models.BigIntegerField(default=0)
    asp8 = models.BigIntegerField(default=0)
    year = models.IntegerField()
    election = models.IntegerField(default=1)
    valid_votes = models.BigIntegerField(default=0)
    rej_votes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'president_result'
        verbose_name = 'County Level President Result'
        verbose_name_plural = 'County Level President Results'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.county)


class Presidential34B(models.Model):
    """Model for Polling Center voters."""

    county = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    reg_voters = models.BigIntegerField(default=0)
    asp1 = models.BigIntegerField(default=0)
    asp2 = models.BigIntegerField(default=0)
    asp3 = models.BigIntegerField(default=0)
    asp4 = models.BigIntegerField(default=0)
    asp5 = models.BigIntegerField(default=0)
    asp6 = models.BigIntegerField(default=0)
    asp7 = models.BigIntegerField(default=0)
    asp8 = models.BigIntegerField(default=0)
    year = models.IntegerField()
    election = models.IntegerField(default=1)
    valid_votes = models.BigIntegerField(default=0)
    rej_votes = models.BigIntegerField(default=0)
    cast_votes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'president_result_34b'
        verbose_name = '34B President Result'
        verbose_name_plural = '34B President Results'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.constituency)
