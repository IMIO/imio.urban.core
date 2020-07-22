# -*- coding: utf-8 -*-

from Products.urban import utils
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL

from datetime import date

from imio.urban.core.testing import IntegrationTestCase

from plone import api
from plone.app.testing import login

import transaction
import unittest2 as unittest


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


class TestParcellingIntegration(IntegrationTestCase):

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

    def test_parcelling_title(self):
        portal = self.layer['portal']
        parcellings = portal.urban.parcellings.objectValues()
        self.assertEquals(len(parcellings), 1)
        parcelling = parcellings[0]
        self.assertEquals(parcelling.portal_type, 'Parcelling')
        self.assertEquals(parcelling.title, u'Lotissement 1 (André Ledieu - 01/01/2005)')


class TestParcelling(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban
        self.parcelling = portal.urban.parcellings.objectValues()[0]
        default_user = self.layer.default_user
        login(self.portal, default_user)
        # create a test CODT_BuildLicence
        self.licence = self._create_test_licence('CODT_BuildLicence')
        transaction.commit()

    def _create_test_licence(self, portal_type, **args):
        licence_folder = utils.getLicenceFolder(portal_type)
        testlicence_id = 'test_{}'.format(portal_type.lower())
        licence_folder.invokeFactory(portal_type, id=testlicence_id)
        test_licence = getattr(licence_folder, testlicence_id)
        return test_licence

    def test_parcelling_referenceable_on_licence(self):
        licence = self.licence
        self.assertFalse(licence.getParcellings())
        parcelling = self.portal.urban.parcellings.p1
        licence.setParcellings(parcelling)
        self.assertEquals(licence.getParcellings(), parcelling)
