# -*- coding: utf-8 -*-

from imio.urban.core import _
from imio.urban.core.contents.eventconfig import EventConfig
from imio.urban.core.contents.eventconfig import IEventConfig
from imio.urban.core.contents.utils import get_fields
from Products.urban.interfaces import IUrbanConfigurationValue

from plone import api
from plone.autoform import directives as form

from z3c.form.browser.orderedselect import OrderedSelectWidget

from zope import schema
from zope.interface import implementer

import logging
logger = logging.getLogger('imio.urban.core: OpinionEventConfig')


class IOpinionEventConfig(IEventConfig, IUrbanConfigurationValue):
    """
    OpinionEventConfig zope schema.
    """

    form.order_after(abbreviation='IBasic.description')
    abbreviation = schema.TextLine(
        title=_(u'abbreviation'),
        required=False,
    )

    form.order_after(recipientName='abbreviation')
    recipientName = schema.TextLine(
        title=_(u'recipientName'),
        required=False,
    )

    form.order_after(function_department='recipientName')
    function_department = schema.TextLine(
        title=_(u'function_department'),
        required=False,
    )

    form.order_after(organization='function_department')
    organization = schema.TextLine(
        title=_(u'organization'),
        required=False,
    )

    form.order_after(dispatchInformation='organization')
    dispatchInformation = schema.TextLine(
        title=_(u'dispatchInformation'),
        required=False,
    )

    form.order_after(typeAndStreetName_number_box='dispatchInformation')
    typeAndStreetName_number_box = schema.TextLine(
        title=_(u'typeAndStreetName_number_box'),
        required=False,
    )

    form.order_after(postcode_locality='typeAndStreetName_number_box')
    postcode_locality = schema.TextLine(
        title=_(u'postcode_locality'),
        required=False,
    )

    form.order_after(country='postcode_locality')
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

    def get_abbreviation(self):
        return self.abbreviation or u''

    def getExtraValue(self):
        """
        Backward compatibility.
        """
        return self.get_abbreviation()

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

    def getExternalDirections(self):
        return self.externalDirections or ()

    def mayAddOpinionRequestEvent(self, inquiry):
        """
        This is used as TALExpression for the UrbanEventOpinionRequest
        We may add an OpinionRequest if we asked one in an inquiry on the licence
        We may add another if another inquiry defined on the licence ask for it and so on
        """
        may_add = inquiry.mayAddOpinionRequestEvent(self.id)
        return may_add

    def to_dict(self):
        dict_ = {
            'id': self.id,
            'UID': self.UID(),
            'enabled': api.content.get_state(self) == 'enabled',
            'portal_type': self.portal_type,
            'title': self.title,
        }
        for field_name, field in get_fields(self):
            val = getattr(self, field_name)
            if val is None:
                val = u''
            if type(val) is str:
                val = val.decode('utf8')
            dict_[field_name] = val
        return dict_
