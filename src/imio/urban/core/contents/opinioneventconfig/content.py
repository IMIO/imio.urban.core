# -*- coding: utf-8 -*-

from imio.urban.core import _
from imio.urban.core.contents.eventconfig import EventConfig
from imio.urban.core.contents.eventconfig import IEventConfig
from imio.urban.core.contents.schemas import IVocabularyTerm
from imio.urban.core.contents.schemas import VocabularyTerm

from plone.autoform import directives as form
from plone.dexterity.schema import DexteritySchemaPolicy

from z3c.form.browser.orderedselect import OrderedSelectWidget

from zope import schema
from zope.interface import implementer

import logging
logger = logging.getLogger('imio.urban.core: OpinionEventConfig')


class IOpinionEventConfig(IEventConfig):
    """
    OpinionEventConfig zope schema.
    """

    form.order_after(abbreviation='description')
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
        required=False,
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


class OpinionEventConfigSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IOpinionEventConfig, IVocabularyTerm)


@implementer(IOpinionEventConfig)
class OpinionEventConfig(EventConfig, VocabularyTerm):
    """
    OpinionEventConfig class
    """

    def __str__(self):
        if self.get_abbreviation():
            if type(self.get_abbreviation()) is unicode:
                return self.get_abbreviation().encode('utf-8')
            return self.get_abbreviation()
        return super(EventConfig, self).__str__()

    def __unicode__(self):
        if self.get_abbreviation():
            if type(self.get_abbreviation()) is unicode:
                return self.get_abbreviation()
            return self.get_abbreviation().decode('utf-8')
        return super(EventConfig, self).__unicode__()

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
