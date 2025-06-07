from django.contrib.gis.db import models


class AdministrativeUnitBoundary(models.Model):

    """Base class for the models that implement administrative boundaries

    All common operations and fields are here.
    We retain the default SRID ( 4326 - WGS84 ).
    """

    # 3 decimal places for the web map ( about 10 meter accuracy )
    PRECISION = 3
    TOLERANCE = (1.0 / 10 ** PRECISION)

    # These two fields should mirror the contents of the relevant admin
    # area model
    # TODO : remove the two fields in CountyBoundary, ConstituencyBoundary and
    # WardBoundary models, retain them in WorldBorder model.
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    # Making this field nullable is a temporary band-aid for a deficiency
    # in model_mommy ( a testing tool )
    # The impact of this is minimal; these models hold setup data that is
    # loaded and tested during each build
    mpoly = models.MultiPolygonField(null=True, blank=True)

    @property
    def bound(self):
        return json.loads(self.mpoly.envelope.geojson) if self.mpoly else None

    @property
    def center(self):
        return json.loads(self.mpoly.centroid.geojson) if self.mpoly else None

    @property
    def surface_area(self):
        return self.mpoly.area if self.mpoly else 0

    @property
    def facility_count(self):
        return FacilityCoordinates.objects.filter(
            coordinates__contained=self.mpoly
        ).count() if self and self.mpoly else 0

    @property
    def density(self):
        """This is a synthetic value

        The units matter less than the relative density compared to other
        administrative units
        """
        return self.facility_count / (self.surface_area * 10000) \
            if self.surface_area else 0

    @property
    def facility_coordinates(self):
        from common.models.model_declarations import \
            _lookup_facility_coordinates
        return _lookup_facility_coordinates(self)

    @property
    def geometry(self):
        """Reduce the precision of the geometries sent in list views

        This produces a MASSIVE saving in rendering time
        """
        if not self.mpoly:
            return self.mpoly

        def _simplify(tolerance, geometry):
            if isinstance(geometry, MultiPolygon):
                polygon = None
                for child_polygon in geometry:
                    if polygon:
                        polygon.extend(child_polygon)
                    else:
                        polygon = child_polygon
            else:
                polygon = geometry

            return json.loads(
                polygon.simplify(tolerance=tolerance).geojson
            )

        geojson_dict = _simplify(
            tolerance=self.TOLERANCE, geometry=self.mpoly.cascaded_union
        )
        original_coordinates = geojson_dict['coordinates']
        assert original_coordinates
        new_coordinates = [
            [
                [
                    round(coordinate_pair[0], self.PRECISION),
                    round(coordinate_pair[1], self.PRECISION)
                ]
                for coordinate_pair in original_coordinates[0]
                if coordinate_pair and
                isinstance(coordinate_pair[0], float) and
                isinstance(coordinate_pair[1], float)
            ]
        ]
        geojson_dict['coordinates'] = new_coordinates
        return geojson_dict

    class Meta:
        abstract = True


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
