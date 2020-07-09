# -*- coding: utf-8 -*-

from plone.dexterity.content import Item
from plone.supermodel import model

from zope.interface import implementer


class IParcellingTerm(model.Schema):
    """
    ParcellingTerm dexterity schema.
    """


@implementer(IParcellingTerm)
class ParcellingTerm(Item):
    """
    ParcellingTerm dexterity class.
    """

    def Title(self):
        """
        """
