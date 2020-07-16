# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG

from imio.urban.core.testing import IntegrationTestCase

from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urban.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.types_tool = api.portal.get_tool('portal_types')

    def test_Parcelling_type_registered(self):
        """Test if Parcelling type is registered in portal_types """
        self.assertTrue(self.types_tool.get('Parcelling'))

    def test_parcelling_workflow(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        self.assertEqual(wf_tool.getChainForPortalType('Parcelling'), ('activation_workflow',))


class TestConfigInstall(IntegrationTestCase):

    layer = URBAN_TESTS_CONFIG

    def test_default_parcellings_created(self):
        portal = self.layer['portal']
        parcellings = portal.urban.parcellings.objectValues()
        self.assertEquals(len(parcellings), 1)
        parcelling = parcellings[0]
        self.assertEquals(parcelling.portal_type, 'Parcelling')
