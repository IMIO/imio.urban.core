# -*- coding: utf-8 -*-

from imio.urban.core import _

from plone.autoform import directives as form
from plone.supermodel import model

from z3c.form.browser.checkbox import SingleCheckBoxWidget
from z3c.form.browser.select import SelectWidget
from z3c.form.browser.text import TextWidget
from zope import schema


class IParcel(model.Schema):
    """
    Parcel dexterity schema.
    """

    form.widget('division', SelectWidget)
    division = schema.Choice(
        title=_(u'Division'),
        description=_(u'urban_label_division'),
        vocabulary='urban.vocabularies.division_names',
        required=True,
    )

    form.widget('section', TextWidget)
    section = schema.TextLine(
        title=_(u'Section'),
        description=_(u'urban_label_section'),
        required=True,
    )

    form.widget('radical', TextWidget)
    radical = schema.TextLine(
        title=_(u'Radical'),
        description=_(u'urban_label_radical'),
        required=False,
    )

    form.widget('bis', TextWidget)
    bis = schema.TextLine(
        title=_(u'Bis'),
        description=_(u'urban_label_bis'),
        required=False,
    )

    form.widget('exposant', TextWidget)
    exposant = schema.TextLine(
        title=_(u'Exposant'),
        description=_(u'urban_label_exposant'),
        required=False,
    )

    form.widget('puissance', TextWidget)
    puissance = schema.TextLine(
        title=_(u'Puissance'),
        description=_(u'urban_label_puissance'),
        required=False,
    )

    form.widget('partie', SingleCheckBoxWidget)
    partie = schema.Bool(
        title=_(u'Partie'),
        description=_(u'urban_label_partie'),
        default=False,
        required=False,
    )

    form.omitted('isOfficialParcel')
    isOfficialParcel = schema.Bool(
        title=_(u'Isofficialparcel'),
        description=_(u'urban_label_isOfficialParcel'),
        default=False,
        required=False,
    )

    form.widget('outdated', SingleCheckBoxWidget)
    outdated = schema.Bool(
        title=_(u'Outdated'),
        description=_(u'urban_label_outdated'),
        default=False,
        required=False,
    )
