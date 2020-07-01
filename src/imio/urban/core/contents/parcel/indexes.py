# -*- coding: utf-8 -*-

from imio.urban.core.contents.parcel.interfaces import IParcel

from plone.indexer import indexer


@indexer(IParcel)
def parcel_not_indexed(obj):
    raise AttributeError()
