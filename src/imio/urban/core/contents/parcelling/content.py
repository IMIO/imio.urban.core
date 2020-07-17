# -*- coding: utf-8 -*-

from imio.urban.core import _

from plone.app import textfield
from plone.dexterity.content import Item
from plone.supermodel import model

from zope import schema
from zope.interface import implementer


class IParcelling(model.Schema):
    """
    Parcelling dexterity schema.
    """

    title = schema.TextLine(
        title=_(u'urban_label_title'),
        required=False,
    )

    label = schema.TextLine(
        title=_(u'urban_label_label'),
        required=True,
    )

    subdividerName = schema.TextLine(
        title=_(u'urban_label_subdividerName'),
        required=True,
    )

    authorizationDate = schema.Date(
        title=_(u'urban_label_authorizationDate'),
        required=False,
    )

    approvalDate = schema.Date(
        title=_(u'urban_label_approvalDate'),
        required=False,
    )

    communalReference = schema.TextLine(
        title=_(u'urban_label_CommunalReference'),
        required=False,
    )

    DGO4Reference = schema.TextLine(
        title=_(u'urban_label_DGO4Reference'),
        required=False,
    )

    numberOfParcels = schema.Int(
        title=_(u'urban_label_numberOfParcels'),
        required=True,
    )

    changesDescription = textfield.RichText(
        title=_(u'urban_label_changesDescription'),
        required=False,
    )


@implementer(IParcelling)
class Parcelling(Item):
    """
    Parcelling dexterity class.
    """
