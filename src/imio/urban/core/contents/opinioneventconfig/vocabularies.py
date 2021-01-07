# -*- coding: utf-8 -*-

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class InternalServices(object):
    """
    List all the defined internal services.
    """

    def __call__(self, context, event_portaltype=''):
        registry = api.portal.get_tool('portal_registry')
        registry_field = registry['Products.urban.interfaces.IInternalOpinionServices.services'] or {}
        internal_services = [(key, value['full_name']) for key, value in registry_field.iteritems()]
        # sort elements by title
        internal_services = sorted(internal_services, key=lambda name: name[1])
        vocabulary = SimpleVocabulary([SimpleTerm(t[0], t[0], t[1]) for t in internal_services])
        return vocabulary


InternalServicesFactory = InternalServices()


class ExternalDirections(object):
    """
    List all the defined internal services.
    """

    def __call__(self, context, event_portaltype=''):
        directions = (
            ('brabant_wallon', 'Brabant wallon'),
            ('eupen', 'Eupen'),
            ('hainaut_1', 'Hainaut 1'),
            ('hainaut_2', 'Hainaut 2'),
            ('liege_1', 'Liège 1'),
            ('liege_2', 'Liège 2'),
            ('luxembourg', 'Luxembourg'),
            ('namur', 'Namur'),
        )
        # sort elements by title
        directions = sorted(directions, key=lambda name: name[1])
        vocabulary = SimpleVocabulary([SimpleTerm(t[0], t[0], t[1]) for t in directions])
        return vocabulary


ExternalDirectionsFactory = ExternalDirections()
