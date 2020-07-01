# -*- coding: utf-8 -*-
"""Setup/installation tests for Parcel."""

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban import utils

from imio.urban.core.testing import IntegrationTestCase

from plone.app.testing import login
from plone import api

import transaction
import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urban.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.types_tool = api.portal.get_tool('portal_types')

    def test_Parcel_type_registered(self):
        """Test if Parcel type is registered in portal_types """
        self.assertTrue(self.types_tool.get('Parcel'))


class TestParcel(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban
        default_user = self.layer.default_user
        login(self.portal, default_user)

        # create a test BuildLicence licence
        self.licences = []
        content_type = 'BuildLicence'
        licence_folder = utils.getLicenceFolder(content_type)
        testlicence_id = 'test_{}'.format(content_type.lower())
        licence_folder.invokeFactory(content_type, id=testlicence_id)
        test_licence = getattr(licence_folder, testlicence_id)
        self.licences.append(test_licence)
        transaction.commit()

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            for licence in self.licences:
                api.content.delete(licence)
        transaction.commit()

    def test_parcel_indexing_on_licence(self):
        licence = self.licences[0]
        catalog = api.portal.get_tool('portal_catalog')

        licence_id = licence.id

        licence_brain = catalog(id=licence_id)[0]
        # so far, the index should be empty as  this licence contains no parcel
        self.assertFalse(licence_brain.parcelInfosIndex)

        # add a parcel1, the index should now contain this parcel reference
        api.content.create(container=licence, type='Parcel', id='parcel1', division='A', section='B', radical='6', exposant='D')
        parcel_1 = licence.parcel1
        licence_brain = catalog(id=licence_id)[0]
        self.assertIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)

        # add a parcel2, the index should now contain the two parcel references
        api.content.create(container=licence, type='Parcel', id='parcel2', division='AA', section='B', radical='69', exposant='E')
        parcel_2 = licence.parcel2
        licence_brain = catalog(id=licence_id)[0]
        self.assertIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), licence_brain.parcelInfosIndex)

        # we remove parcel1, the ref of parcel2 should be the only remaining
        # one, the index
        licence.manage_delObjects(['parcel1'])
        licence_brain = catalog(id=licence_id)[0]
        self.assertNotIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), licence_brain.parcelInfosIndex)

    def test_parcel_events(self):
        licence = self.licences[0]

        parcel = api.content.create(container=licence, type='Parcel', id='parcel1', division='A', section='B', radical='6', exposant='D')
        # isOfficialParcel should be False
        self.assertEquals(parcel.isOfficialParcel, False)

    def test_parcel_workflow(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        self.assertEquals(wf_tool.getChainForPortalType('Parcel'), ('one_state_workflow',))

    def test_parcel_redirectsview(self):
        licence = self.licences[0]
        parcel = api.content.create(container=licence, type='Parcel', id='parcel1', division='A', section='B', radical='6', exposant='D')
        parcel_view = parcel.restrictedTraverse('view')
        view_result = parcel_view()
        # default parcel view should redirects to the parent container
        self.assertEquals(view_result, licence.absolute_url())

    def test_divisionCode_field(self):
        licence = self.licences[0]
        parcel = api.content.create(container=licence, type='Parcel', id='parcel1', division='69696', section='B', radical='6', exposant='D')
        # divisionCode should always return the value contained in the field division.
        self.assertEquals(parcel.getDivisionCode(), parcel.getDivision())
        self.assertEquals(parcel.divisionCode, parcel.getDivision())
