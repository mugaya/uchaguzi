import os
from django.contrib.gis.utils import LayerMapping
from .models import WardMaps

mapping = {
    'gid': 'gid',
    'pop2009': 'pop2009',
    'county': 'county',
    'subcounty': 'subcounty',
    'ward': 'ward',
    'uid': 'uid',
    'scuid': 'scuid',
    'cuid': 'cuid',
    'geom': 'MULTIPOLYGON',
}

adm_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'Kenya_Wards',
                 'kenya_wards.shp'),
)


def run(verbose=True):
    lm = LayerMapping(
        WardMaps, adm_shp, mapping,
        transform=False, encoding='utf-8',
    )
    lm.save(strict=True, verbose=verbose)
