# -*- coding: utf-8 -*-
"""Setup/installation tests for ParcellingTerm."""

from imio.urban.core.testing import IntegrationTestCase

from plone import api



class TestInstall(IntegrationTestCase):
    """Test installation of imio.urban.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.types_tool = api.portal.get_tool('portal_types')

    def test_ParcellingTerm_type_registered(self):
        """Test if ParcellingTerm type is registered in portal_types """
        self.assertTrue(self.types_tool.get('ParcellingTerm'))

    def test_parcellingterm_workflow(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        self.assertEqual(wf_tool.getChainForPortalType('ParcellingTerm'), ('one_state_workflow',))
