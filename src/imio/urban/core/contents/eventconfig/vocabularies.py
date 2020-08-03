# -*- coding: utf-8 -*-

from imio.urban.core.contents.eventconfig import IEventConfig
from imio.urban.core.utils import get_portal_type_class

from plone import api

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.urban.UrbanEvent import UrbanEvent
from Products.urban.interfaces import IEventTypeType
from Products.urban.interfaces import ILicenceConfig

from zope.component import getGlobalSiteManager
from zope.i18n import translate
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class EventPortalTypesVocabulary(object):
    """
    Vocabulary listing all the UrbanEvent portal types.
    """

    def __call__(self, context):
        types_tool = api.portal.get_tool('portal_types')

        types_to_check = types_tool.objectIds()

        licence_config = None
        parent = context
        while not IPloneSiteRoot.providedBy(parent):
            parent = parent.aq_parent
            if ILicenceConfig.providedBy(parent):
                licence_config = parent

        # make sure to only return types allowed for this EventConfig licence
        if licence_config:
            for type_definition in types_tool.objectValues():
                if type_definition.id.lower() == licence_config.id:
                    types_to_check = [t for t in types_to_check if t in type_definition.allowed_content_types]
                    break

        terms = []
        for type_id in types_to_check:
            klass = get_portal_type_class(type_id)
            if klass and issubclass(klass, UrbanEvent):
                terms.append(SimpleTerm(type_id, type_id, _(type_id)))

        vocabulary = SimpleVocabulary(terms)
        return vocabulary


EventPortalTypesVocabularyFactory = EventPortalTypesVocabulary()


class EventOptionalFields(object):
    """
    Vocabulary listing all the optional fields of the selected.
    Only implemented for AT UrbanEvent, to reimplements once
    UrbanEvent are migrated to DX.
    """

    def __call__(self, context, event_portaltype=''):
        # try to find the UrbanEvent portal_type on the EventConfig
        if not event_portaltype:
            if IEventConfig.providedBy(context):
                event_portaltype = context.getEventPortalType()
            else:
                event_portaltype = 'UrbanEvent'

        klass = get_portal_type_class(event_portaltype)
        optional_fields = []
        fields = klass.schema.fields()
        for field in fields:
            if getattr(field, 'optional', False):
                optional_fields.append(
                    (
                        field.getName(),
                        translate(
                            field.widget.label,
                            'urban', default=field.getName(),
                            context=context.REQUEST
                        )
                    )
                )
        # sort elements by title
        optional_fields = sorted(optional_fields, key=lambda name: name[1])
        vocabulary = SimpleVocabulary([SimpleTerm(t[0], t[0], t[1]) for t in optional_fields])
        return vocabulary


EventOptionalFieldsFactory = EventOptionalFields()


class EventTypes(object):

    def __call__(self, context):
        gsm = getGlobalSiteManager()
        interfaces = gsm.getUtilitiesFor(IEventTypeType)

        event_types = []
        for name, interface in interfaces:
            event_types.append(
                (
                    name,
                    interface.__doc__,
                    translate(
                        msgid=interface.__doc__,
                        domain='urban',
                        context=context.REQUEST,
                        default=interface.__doc__
                    )
                )
            )
        # sort elements by title
        event_types = sorted(event_types, key=lambda name: name[2])
        vocabulary = SimpleVocabulary([SimpleTerm(t[0], t[1], t[2]) for t in event_types])
        return vocabulary


EventTypesFactory = EventTypes()
