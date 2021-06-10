# -*- coding: utf-8 -*-

from imio.urban.core.contents.eventconfig import IEventConfig
from imio.urban.core.contents.utils import get_portal_type_class

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


class EventConfigVocabulary(object):
    """
    Base class for EventConfig vocabularies
    """

    def get_event_portaltype(self, context):
        if IEventConfig.providedBy(context):
            return context.getEventPortalType()
        else:
            return 'UrbanEvent'

    def get_enabled_fields(self, context):
        if IEventConfig.providedBy(context):
            return context.getActivatedFields()
        else:
            return []


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


class EventOptionalFields(EventConfigVocabulary):
    """
    List all the possible optional fields, the list depends on the EventConfig
    eventPortalType field value.
    [DX] to reimplements once UrbanEvent are migrated to DX! [DX]
    """

    def __call__(self, context, event_portaltype=''):
        event_portaltype = event_portaltype or self.get_event_portaltype(context)
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
    """
    List all the evenType marker interfaces.
    """

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


class EventKeyDates(EventConfigVocabulary):
    """
    List all the enabled dates of this eventConfig.
    """

    def __call__(self, context):
        event_portaltype = self.get_event_portaltype(context)
        enabled_fields = self.get_enabled_fields(context)
        klass = get_portal_type_class(event_portaltype)
        all_fields = klass.schema.getSchemataFields('default')
        date_fields = []
        for field in all_fields:
            is_date_field = field.getType() == 'Products.Archetypes.Field.DateTimeField'
            if is_date_field:
                fieldname = field.getName()
                enabled = fieldname in enabled_fields
                if getattr(field, 'optional', False) and enabled or not hasattr(field, 'optional'):
                    date_fields.append(
                        (
                            fieldname,
                            translate(
                                "urban_label_" + fieldname,
                                'urban',
                                default=fieldname,
                                context=context.REQUEST
                            )
                        )
                    )
        # sort elements by title
        date_fields = sorted(date_fields, key=lambda name: name[1])
        vocabulary = SimpleVocabulary([SimpleTerm(d[0], d[0], d[1]) for d in date_fields])
        return vocabulary


EventKeyDatesFactory = EventKeyDates()


class EventTextFields(EventConfigVocabulary):
    """
    List all the possible text fields.
    [DX] implemented for AT.TextField, to rewrite once UrbanEvent is migrated to DX [DX]
    """

    def __call__(self, context):
        request = api.portal.getRequest()
        # hack to get the eventConfig as context, since context is <NO_VALUE> in a
        # datagrid
        if not IEventConfig.providedBy(context):
            context = request.PARENTS[0]
        event_portaltype = self.get_event_portaltype(context)
        klass = get_portal_type_class(event_portaltype)
        all_fields = klass.schema.getSchemataFields('default')
        text_fields = []
        exclude = ['rights']
        for field in all_fields:
            is_text_field = field.getType() == 'Products.Archetypes.Field.TextField'
            fieldname = field.getName()
            if is_text_field and fieldname not in exclude:
                text_fields.append(
                    (
                        fieldname,
                        translate(
                            "urban_label_" + fieldname,
                            'urban',
                            default=fieldname,
                            context=request
                        )
                    )
                )
        # sort elements by title
        text_fields = sorted(text_fields, key=lambda name: name[1])
        vocabulary = SimpleVocabulary([SimpleTerm(d[0], d[0], d[1]) for d in text_fields])
        return vocabulary


EventTextFieldsFactory = EventTextFields()
