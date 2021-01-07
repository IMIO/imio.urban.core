# -*- coding: utf-8 -*-

from plone import api
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI

from zope.component import getUtility


def get_portal_type_class(portal_type):
    """
    Return the class of the given portal_type.
    Implemented for both AT and DX but should only keep DX once
    the urban DX migration is complete.
    """
    types_tool = api.portal.get_tool('portal_types')
    type_definition = getattr(types_tool, portal_type)
    # dexterity
    if hasattr(type_definition, 'klass'):
        klass_path = '.'.join(type_definition.klass.split('.')[:-1])
        klass_name = type_definition.klass.split('.')[-1]
        klass_module = __import__(klass_path, fromlist=[klass_name])
        klass = getattr(klass_module, klass_name)
    # Archetype, to delete later
    else:
        at_tool = api.portal.get_tool('archetype_tool')
        module = [at_def for at_def in at_tool.listRegisteredTypes()
                  if at_def['portal_type'] == type_definition.id]
        module = module or [at_def for at_def in at_tool.listRegisteredTypes()
                            if at_def['meta_type'] == type_definition.content_meta_type]
        klass = module and module[0]['klass']
    return klass


def get_fields(dx_object):
    fti = getUtility(IDexterityFTI, name=dx_object.portal_type)
    fti_schema = fti.lookupSchema()
    fields = [(n, f) for n, f in fti_schema.namesAndDescriptions(all=True)]

    # also lookup behaviors
    for behavior_id in fti.behaviors:
        behavior = getUtility(IBehavior, behavior_id).interface
        fields.extend([(n, f) for n, f in behavior.namesAndDescriptions(all=True)])

    return fields
