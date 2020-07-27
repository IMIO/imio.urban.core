# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase

from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of EventConfig."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.types_tool = api.portal.get_tool('portal_types')

    def test_EventConfig_type_registered(self):
        """Test if EventConfig type is registered in portal_types """
        self.assertTrue(self.types_tool.get('EventConfig'))

    def test_parcelling_workflow(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        self.assertEqual(wf_tool.getChainForPortalType('EventConfig'), ('activation_workflow',))
