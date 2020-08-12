# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase

from plone import api
from plone.app.testing import login
from Products.urban.interfaces import IUrbanEvent
from Products.urban.testing import URBAN_TESTS_LICENCES

import unittest


class TestInstall(IntegrationTestCase):
    """Test installation of OpinionEventConfig."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.types_tool = api.portal.get_tool('portal_types')

    def test_OpinionEventConfig_type_registered(self):
        """Test if OpinionEventConfig type is registered in portal_types """
        self.assertTrue(self.types_tool.get('OpinionEventConfig'))

    def test_parcelling_workflow(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        self.assertEqual(wf_tool.getChainForPortalType('OpinionEventConfig'), ('activation_workflow',))


class TestUrbanEventTypes(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        login(portal, 'urbaneditor')
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        self.catalog = api.portal.get_tool('portal_catalog')
        buildlicence_brains = self.catalog(portal_type='BuildLicence', Title='Exemple Permis Urbanisme')
        self.buildlicence = buildlicence_brains[0].getObject()
        self.event_configs = self.portal_urban.buildlicence.eventconfigs

    def test_getLinkedUrbanEvents(self):
        """
        For each OpinionEventConfig, at least one event should have been created and can be found
        with 'getLinkedUrbanEvents' method.
        """
        for event_config in self.event_configs.objectValues():
            linked_urbanevents = event_config.getLinkedUrbanEvents()
            if event_config.canBeCreatedInLicence(self.buildlicence):
                self.assertEqual(len(linked_urbanevents), 1)
                self.assertEqual(linked_urbanevents[0].getUrbaneventtypes(), event_config)
                self.assertTrue(IUrbanEvent.providedBy(linked_urbanevents[0]))
