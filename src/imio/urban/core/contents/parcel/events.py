# -*- coding: utf-8 -*-

from Products.urban import services
from Products.urban.events import licenceEvents
from Products.urban.interfaces import IGenericLicence


def set_authenticity(parcel, event):
    """
     Check if the manually added parcel exists in he cadastral DB
     and set its 'isOfficialParcel' attribute accordingly.
    """
    parcel_status = False
    try:
        cadastre = services.cadastre.new_session()
        parcel_status = cadastre.get_parcel_status(parcel.capakey)
        cadastre.close()
    except services.cadastral.UnreferencedParcelError:
        pass

    parcel.isOfficialParcel = parcel_status in ['old_parcel', 'actual_parcel']
    parcel.outdated = parcel_status in ['old_parcel']
    parcel.reindexObject()


def update_container_parcelindex(parcel, event):
    """
    Reindex parcel container after creation/modification/deletion.
    """
    parcel.aq_inner.aq_parent.reindexObject(idxs=["parcelInfosIndex"])


def update_bound_licences_parcelindex(parcel, container=None, events=[]):
    """
    If ticket or inspection refers to the parcel licence, update their
    parcelInfosIndex as well when the parcel is modified/deleted/created.
    """
    licence = getattr(parcel, 'aq_parent', container)
    if not IGenericLicence.providedBy(licence):
        licence = getattr(licence, 'aq_parent', container)
    # only update if the parent is a licence.
    if not IGenericLicence.providedBy(licence):
        return
    licenceEvents._updateBoundLicencesIndexes(
        licence, events, indexes=['parcelInfosIndex']
    )
