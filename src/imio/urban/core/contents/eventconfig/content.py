# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridField
from collective.z3cform.datagridfield import DictRow

from imio.urban.core import _

from plone.app import textfield
from plone.autoform import directives as form
from plone.dexterity.content import Container
# from plone.formwidget.masterselect import MasterSelectField
from plone.supermodel import model

from z3c.form.browser.orderedselect import OrderedSelectWidget
from z3c.form.browser.select import SelectWidget

from zope import interface
from zope import schema
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

    form.widget('eventPortalType', SelectWidget)
    eventPortalType = schema.Choice(
        title=_(u'eventPortalType'),
        vocabulary='urban.vocabularies.event_portaltypes',
        required=True,
    )

    form.widget('activatedFields', OrderedSelectWidget)
    activatedFields = schema.Choice(
        title=_(u'activatedFields'),
        vocabulary='urban.vocabularies.division_names',
        required=True,
    )

    form.widget('eventType', OrderedSelectWidget)
    eventType = schema.Choice(
        title=_(u'eventType'),
        vocabulary='urban.vocabularies.division_names',
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
