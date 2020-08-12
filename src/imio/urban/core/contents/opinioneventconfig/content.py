# -*- coding: utf-8 -*-

from imio.urban.core import _
from imio.urban.core.contents.eventconfig import EventConfig
from imio.urban.core.contents.eventconfig import IEventConfig

from plone.autoform import directives as form

from z3c.form.browser.orderedselect import OrderedSelectWidget

from zope import schema
from zope.interface import implementer

import logging
logger = logging.getLogger('imio.urban.core: OpinionEventConfig')


class IOpinionEventConfig(IEventConfig):
    """
    OpinionEventConfig zope schema.
    """

    recipientName = schema.TextLine(
        title=_(u'recipientName'),
        required=False,
    )

    function_department = schema.TextLine(
        title=_(u'function_department'),
        required=False,
    )

    organization = schema.TextLine(
        title=_(u'organization'),
        required=False,
    )

    dispatchInformation = schema.TextLine(
        title=_(u'dispatchInformation'),
        required=False,
    )

    typeAndStreetName_number_box = schema.TextLine(
        title=_(u'typeAndStreetName_number_box'),
        required=False,
    )

    postcode_locality = schema.TextLine(
        title=_(u'postcode_locality'),
        required=False,
    )

    country = schema.TextLine(
        title=_(u'country'),
        required=False,
    )

    is_internal_service = schema.Bool(
        title=_(u'is_internal_service'),
        default=False,
        required=False,
    )

    internal_service = schema.Choice(
        title=_(u'internal_service'),
        vocabulary='urban.vocabularies.internal_services',
        required=True,
        default='UrbanEvent',
    )

    form.widget('externalDirections', OrderedSelectWidget)
    externalDirections = schema.Tuple(
        title=_(u'externalDirections'),
        value_type=schema.Choice(
            vocabulary='urban.vocabularies.external_directions',
        ),
        required=False,
    )


@implementer(IOpinionEventConfig)
class OpinionEventConfig(EventConfig):
    """
    OpinionEventConfig class
    """

    def getRecipientName(self):
        return self.recipientName or u''

    def getFunction_department(self):
        return self.function_department or u''

    def getOrganization(self):
        return self.organization or u''

    def getDispatchInformation(self):
        return self.dispatchInformation or u''

    def getTypeAndStreetName_number_box(self):
        return self.typeAndStreetName_number_box or u''

    def getPostcode_locality(self):
        return self.postcode_locality or u''

    def getCountry(self):
        return self.country or u''

    def getIs_internal_service(self):
        return self.is_internal_service or False

    def getInternal_service(self):
        return self.internal_service or u''

    def getExternal_directions(self):
        return self.external_directions or ()

    def mayAddOpinionRequestEvent(self, inquiry):
        """
        This is used as TALExpression for the UrbanEventOpinionRequest
        We may add an OpinionRequest if we asked one in an inquiry on the licence
        We may add another if another inquiry defined on the licence ask for it and so on
        """
        may_add = inquiry.mayAddOpinionRequestEvent(self.id)
        return may_add
