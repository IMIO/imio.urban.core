# -*- coding: utf-8 -*-
from imio.urban.core.contents.parcelling import IParcelling
from plone.indexer import indexer


@indexer(IParcelling)
def parcelling_parcelinfoindex(obj):
    """
    Index parcels of a parcelling term
    """
    parcels_infos = []
    if hasattr(obj, 'getParcels'):
        parcels_infos = list(set([p.get_capakey() for p in obj.getParcels()]))
    return parcels_infos
