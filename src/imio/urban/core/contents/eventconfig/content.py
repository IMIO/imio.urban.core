# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridField
from collective.z3cform.datagridfield import DictRow

from imio.urban.core import _

from plone import api
from plone.app import textfield
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.supermodel import model

from Products.CMFCore.Expression import Expression
from Products.PageTemplates.Expressions import getEngine
from Products.urban.docgen.UrbanTemplate import IUrbanTemplate

from z3c.form.browser.orderedselect import OrderedSelectWidget

from zope import interface
from zope import schema
from zope.component import getUtility
from zope.interface import implementer

import logging
logger = logging.getLogger('imio.urban.core: EventConfig')


class IDefaultTextRowSchema(interface.Interface):
    """
    Schema for defaultText datagridfield row.
    """
    fieldname = schema.Choice(
        title=u"Fieldname",
        vocabulary='urban.vocabularies.event_text_fields',
    )

    text = schema.Text(
        title=u"Text"
    )


def getActivableFields(portal_type):
    """
    Vocabulary method for master select widget (not working)
    """
    vocabulary = getUtility(schema.interfaces.IVocabularyFactory, 'urban.vocabularies.event_optionalfields')
    portal = api.portal.get()
    voc = vocabulary(portal, portal_type)
    return voc


class IEventConfig(model.Schema):
    """
    EventConfig zope schema.
    """

    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    showTitle = schema.Bool(
        title=_(u'showTitle'),
        default=False,
        required=False,
    )

    eventDateLabel = schema.TextLine(
        title=_(u'eventDateLabel'),
        required=False,
    )

    description = textfield.RichText(
        title=_PMF(u'label_description', default=u'Summary'),
        description=_PMF(
            u'help_description',
            default=u'Used in item listings and search results.'
        ),
        required=False,
        default=textfield.RichTextValue(''),
        missing_value=u'',
    )

    eventPortalType = schema.Choice(
        title=_(u'eventPortalType'),
        vocabulary='urban.vocabularies.event_portaltypes',
        required=True,
        default='UrbanEvent',
    )

    form.widget('activatedFields', OrderedSelectWidget, size=20)
    activatedFields = schema.Tuple(
        title=_(u'activatedFields'),
        value_type=schema.Choice(
            vocabulary='urban.vocabularies.event_optionalfields',
        ),
        required=True,
    )

    form.widget('eventType', OrderedSelectWidget, size=20)
    eventType = schema.Tuple(
        title=_(u'eventType'),
        value_type=schema.Choice(
            vocabulary='urban.vocabularies.event_types',
        ),
        required=False,
    )

    isKeyEvent = schema.Bool(
        title=_(u'isKeyEvent'),
        default=False,
        required=False,
    )

    form.widget('keyDates', OrderedSelectWidget)
    keyDates = schema.Tuple(
        title=_(u'keyDates'),
        value_type=schema.Choice(
            vocabulary='urban.vocabularies.event_enabled_dates',
        ),
        required=False,
    )

    TALCondition = schema.TextLine(
        title=_(u'TALCondition'),
        required=False,
    )

    form.widget('textDefaultValues', DataGridField)
    textDefaultValues = schema.List(
        title=_(u'textDefaultValues'),
        value_type=DictRow(title=u"tablerow", schema=IDefaultTextRowSchema),
        required=False,
    )


@implementer(IEventConfig)
class EventConfig(Container):
    """
    EventConfig class
    """

    def Description(self):
        if self.description:
            if type(self.description) is unicode:
                return self.description.encode('utf-8')
            raw = self.description.raw
            if type(raw) is unicode:
                return raw.encode('utf-8')
        return textfield.RichTextValue('').raw

    def getShowTitle(self):
        return self.showTitle or False

    def getEventDateLabel(self):
        return self.eventDateLabel or u'Date'

    def getEventPortalType(self):
        return self.eventPortalType or u''

    def getActivatedFields(self):
        return self.activatedFields or ()

    def getEventType(self):
        return self.eventType or ()

    def getIsKeyEvent(self):
        return self.isKeyEvent or False

    def getKeyDates(self):
        return self.keyDates or ()

    def getTALCondition(self):
        return self.TALCondition or u''

    def getTextDefaultValues(self):
        return self.textDefaultValues or []

    def getTemplates(self):
        """
        Return contained POD templates.
        """
        templates = [obj for obj in self.objectValues() if IUrbanTemplate.providedBy(obj)]
        return templates

    def getLinkedUrbanEvents(self):
        """
        Return all the urban events linked to this urban event type.
        """
        ref_catalog = api.portal.get_tool('reference_catalog')
        ref_brains = ref_catalog(targetUID=self.UID())
        urban_events = [ref_brain.getObject().getSourceObject() for ref_brain in ref_brains]
        return urban_events

    def canBeCreatedInLicence(self, obj):
        """
        Creation condition

        computed by evaluating the TAL expression stored in TALCondition field
        """
        res = True  # At least for now
        # Check condition
        TALCondition = self.getTALCondition().strip()
        if TALCondition:
            data = {
                'nothing': None,
                'portal': api.portal.get(),
                'object': obj,
                'event': self,
                'request': api.portal.getRequest(),
                'here': obj,
                'licence': obj,
            }
            ctx = getEngine().getContext(data)
            try:
                res = Expression(TALCondition)(ctx)
            except Exception, e:
                logger.warn("The condition '%s' defined for element at '%s' is wrong!\
Message is : %s" % (TALCondition, obj.absolute_url(), e))
                res = False
        return res

    def checkCreationInLicence(self, obj):
        if not self.canBeCreatedInLicence(obj):
            raise ValueError(_("You can not create this UrbanEvent !"))

    def mayAddInspectionReportEvent(self, licence):
        """
        """
        may_add = licence.mayAddInspectionReportEvent()
        return may_add
