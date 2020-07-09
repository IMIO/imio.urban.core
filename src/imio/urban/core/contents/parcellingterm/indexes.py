# -*- coding: utf-8 -*-
from imio.urban.core.contents.parcellingterm import IParcellingTerm
from plone.indexer import indexer


@indexer(IParcellingTerm)
def parcellingterm_parcelinfoindex(obj):
    """
    Index parcels of a parcelling term
    """
    parcels_infos = []
    if hasattr(obj, 'getParcels'):
        parcels_infos = list(set([p.get_capakey() for p in obj.getParcels()]))
    return parcels_infos