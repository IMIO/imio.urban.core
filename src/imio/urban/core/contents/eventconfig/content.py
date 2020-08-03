# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridField
from collective.z3cform.datagridfield import DictRow

from imio.urban.core import _

from plone import api
from plone.app import textfield
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.masterselect import MasterSelectField
from plone.supermodel import model

from z3c.form.browser.orderedselect import OrderedSelectWidget

from zope import interface
from zope import schema
from zope.component import getUtility
from zope.interface import implementer


class IDefaultTextRowSchema(interface.Interface):
    """
    Schema for defaultText datagridfield row.
    """
    fieldname = schema.Choice(
        title=u"Fieldname",
        vocabulary='urban.vocabularies.division_names',
    )

    text = textfield.RichText(title=u"Text")


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

    showTitle = schema.Bool(
        title=_(u'showTitle'),
        default=False,
        required=False,
    )

    eventDateLabel = schema.TextLine(
        title=_(u'eventDateLabel'),
        required=False,
    )

    # master select not working yet
    eventPortalType = MasterSelectField(
        title=_(u'eventPortalType'),
        vocabulary='urban.vocabularies.event_portaltypes',
        slave_fields=(
            # Controls the vocab of activatedFields
            {
                'name': 'activatedFields',
                'action': 'vocabulary',
                'vocab_method': getActivableFields,
                'control_param': 'portal_type',
            },
        ),
        required=True,
    )

    form.widget('activatedFields', OrderedSelectWidget)
    activatedFields = schema.Set(
        title=_(u'activatedFields'),
        value_type=schema.Choice(
            vocabulary='urban.vocabularies.event_optionalfields',
        ),
        required=True,
    )

    form.widget('eventType', OrderedSelectWidget)
    eventType = schema.Choice(
        title=_(u'eventType'),
        vocabulary='urban.vocabularies.event_types',
        required=False,
    )

    isKeyEvent = schema.Bool(
        title=_(u'isKeyEvent'),
        default=False,
        required=False,
    )

    form.widget('keyDates', OrderedSelectWidget)
    keyDates = schema.Choice(
        title=_(u'keyDates'),
        vocabulary='urban.vocabularies.division_names',
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

    def getEventPortalType(self):
        return getattr(self, 'eventPortalType', '')
