# -*- coding: utf-8 -*-

from Products.urban import utils
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL

from datetime import date

from imio.urban.core.testing import IntegrationTestCase
from imio.urban.core.tests.helpers import BrowserTestCase

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

import transaction
import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of Parcelling."""

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

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.parcellings = self.portal.urban.parcellings.objectValues()

    def test_default_parcellings_created(self):
        parcellings = self.parcellings
        self.assertEquals(len(parcellings), 1)
        parcelling = parcellings[0]
        self.assertEquals(parcelling.portal_type, 'Parcelling')
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (André Ledieu - 01/01/2005 - 12/01/2005)')
        self.assertEquals(parcelling.label, u'Lotissement 1')
        self.assertEquals(parcelling.subdividerName, u'André Ledieu')
        self.assertEquals(parcelling.approvalDate, date(2005, 1, 12))
        self.assertEquals(parcelling.authorizationDate, date(2005, 1, 1))
        self.assertEquals(parcelling.numberOfParcels, 10)

    def test_parcelling_allowed_types(self):
        parcellings = self.parcellings
        self.assertEquals(len(parcellings), 1)
        parcelling = parcellings[0]
        login(self.portal, 'urbaneditor')
        self.assertEquals(parcelling.allowedContentTypes()[0].getId(), 'Parcel')

    def test_parcelling_title(self):
        parcellings = self.parcellings
        self.assertEquals(len(parcellings), 1)
        parcelling = parcellings[0]
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (André Ledieu - 01/01/2005 - 12/01/2005)')


class TestParcellingView(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.parcellings = self.portal.urban.parcellings.objectValues()
        self.parcelling = self.portal.urban.parcellings.objectValues()[0]
        self.browser = Browser(self.portal)
        default_user = self.layer.default_user
        default_password = self.layer.default_password
        self.browserLogin(default_user, default_password)

    def test_parcels_listing_visible_on_parcelling_view(self):
        self.browser.open(self.parcelling.absolute_url())
        contents = self.browser.contents
        self.assertIn('Parcelle(s)', contents, msg='parcels listing is not visible')

    def test_date_widget_min_value_1960(self):
        self.browser.open(self.parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        self.assertIn('<option value="1960">1960</option>', contents, msg='The minimum date value is not 1960')


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
        parcelling = self.parcelling
        licence.setParcellings(parcelling)
        self.assertEquals(licence.getParcellings(), parcelling)

    def test_parcelling_title_with_parcels(self):
        parcelling = self.parcelling
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (André Ledieu - 01/01/2005 - 12/01/2005)')
        login(self.portal, 'urbaneditor')
        parcel_1 = api.content.create(
            container=parcelling, type='Parcel', id='parcel1',
            division=u'A', section=u'B', radical=u'6', exposant=u'D'
        )
        self.assertIn("A B 6", parcelling.Title())

    def test_get_parcels_method(self):
        parcelling = self.parcelling
        login(self.portal, 'urbaneditor')
        parcel_1 = api.content.create(
            container=parcelling, type='Parcel', id='parcel1',
            division=u'A', section=u'B', radical=u'6', exposant=u'D'
        )
        self.assertEquals(parcelling.get_parcels(), [parcel_1])

