# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG

from datetime import date

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


class TestParcellingConfigInstall(IntegrationTestCase):

    layer = URBAN_TESTS_CONFIG

    def test_default_parcellings_created(self):
        portal = self.layer['portal']
        parcellings = portal.urban.parcellings.objectValues()
        self.assertEquals(len(parcellings), 1)
        parcelling = parcellings[0]
        self.assertEquals(parcelling.portal_type, 'Parcelling')
        self.assertEquals(parcelling.title, u'Lotissement 1 (André Ledieu - 01/01/2005)')
        self.assertEquals(parcelling.label, u'Lotissement 1')
        self.assertEquals(parcelling.subdividerName, u'André Ledieu')
        self.assertEquals(parcelling.approvalDate, date(2005, 1, 12))
        self.assertEquals(parcelling.authorizationDate, date(2005, 1, 1))
        self.assertEquals(parcelling.numberOfParcels, 10)
