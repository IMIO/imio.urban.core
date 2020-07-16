# -*- coding: utf-8 -*-

from imio.urban.core import _

from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.supermodel import model

from z3c.form.browser.text import TextWidget
from z3c.form.browser.textarea import TextAreaWidget

from zope import schema
from zope.interface import implementer


class IParcelling(model.Schema):
    """
    Parcelling dexterity schema.
    """

    form.widget('title', TextWidget)
    title = schema.TextLine(
        title=_(u'urban_label_title'),
        required=False,
    )

    form.widget('label', TextWidget)
    label = schema.TextLine(
        title=_(u'urban_label_label'),
        required=True,
    )

    form.widget('subdividerName', TextWidget)
    subdividerName = schema.TextLine(
        title=_(u'urban_label_subdividerName'),
        required=True,
    )

    form.widget('authorizationDate')
    authorizationDate = schema.Datetime(
        title=_(u'urban_label_authorizationDate'),
        required=False,
    )

    form.widget('approvalDate')
    approvalDate = schema.Datetime(
        title=_(u'urban_label_approvalDate'),
        required=False,
    )

    form.widget('communalReference', TextWidget)
    communalReference = schema.TextLine(
        title=_(u'urban_label_CommunalReference'),
        required=False,
    )

    form.widget('DGO4Reference', TextWidget)
    DGO4Reference = schema.TextLine(
        title=_(u'urban_label_DGO4Reference'),
        required=False,
    )

    form.widget('numberOfParcels')
    numberOfParcels = schema.Int(
        title=_(u'urban_label_numberOfParcels'),
        required=True,
    )

    form.widget('changesDescription', TextAreaWidget)
    changesDescription = schema.TextLine(
        title=_(u'urban_label_changesDescription'),
        required=False,
    )


@implementer(IParcelling)
class Parcelling(Item):
    """
    Parcelling dexterity class.
    """
