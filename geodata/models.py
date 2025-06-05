from django.contrib.gis.db import models


class WardMaps(models.Model):
    gid = models.BigIntegerField()
    pop2009 = models.FloatField()
    county = models.CharField(max_length=40)
    subcounty = models.CharField(max_length=80)
    ward = models.CharField(max_length=80)
    uid = models.CharField(max_length=12, null=True)
    scuid = models.CharField(max_length=11, null=True)
    cuid = models.CharField(max_length=11, null=True)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'ward_maps'
        verbose_name = 'Ward Map'
        verbose_name_plural = 'Ward Maps'

    def __str__(self):
        return self.ward
