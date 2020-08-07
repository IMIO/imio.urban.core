# -*- coding: utf-8 -*-

from plone import api


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
        if not module:
            return
        klass = module[0]['klass']
    return klass
