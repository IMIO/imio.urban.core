# -*- coding: utf-8 -*-

from imio.urban.core import _

from plone.dexterity.content import Container
from plone.supermodel import model

from zope import schema
from zope.interface import implementer


class IEventConfig(model.Schema):
    """
    EventConfig zope schema.
    """

    label = schema.TextLine(
        title=_(u'urban_label_label'),
        required=True,
    )


@implementer(IEventConfig)
class EventConfig(Container):
    """
    EventConfig class
    """
