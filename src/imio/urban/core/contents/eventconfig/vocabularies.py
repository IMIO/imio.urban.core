# -*- coding: utf-8 -*-

from plone import api

from Products.CMFPlone import PloneMessageFactory as _
from Products.urban.interfaces import ILicenceConfig
from Products.urban.UrbanEvent import UrbanEvent

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class EventPortalTypesVocabulary(object):
    """
    Vocabulary listing all the UrbanEvent portal types.
    """

    def __call__(self, context):
        types_tool = api.portal.get_tool('portal_types')
        at_tool = api.portal.get_tool('archetype_tool')

        # make sure to only return types allowed for this EventConfig licence
        types_to_check = types_tool.objectValues()
        if ILicenceConfig.providedBy(context.aq_parent):
            licence_config = context.aq_parent
            for type_definition in types_tool.objectValues():
                if type_definition.id.lower() == licence_config.id:
                    types_to_check = [t for t in types_to_check if t.id in type_definition.allowed_content_types]
                    break

        terms = []
        for type_definition in types_to_check:
            # handle case of both Archetypes and dexterity, delete this if/else once
            # all the Archetypes content is migrated to DX
            if hasattr(type_definition, 'klass'):
                klass_path = '.'.join(type_definition.klass.split('.')[:-1])
                klass_name = type_definition.klass.split('.')[-1]
                klass_module = __import__(klass_path, fromlist=[klass_name])
                klass = getattr(klass_module, klass_name)
            else:
                modules = [at_def for at_def in at_tool.listRegisteredTypes()
                           if at_def['portal_type'] == type_definition.id]
                if modules:
                    klass = modules[0]['klass']
                else:
                    continue
            if issubclass(klass, UrbanEvent):
                terms.append((type_definition.id, type_definition.id, _(type_definition.id)))

        vocabulary = SimpleVocabulary([SimpleTerm(t[0], t[1], t[2]) for t in terms])
        return vocabulary


EventPortalTypesVocabularyFactory = EventPortalTypesVocabulary()
