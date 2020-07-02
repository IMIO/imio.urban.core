# -*- coding: utf-8 -*-
"""Setup/installation tests for Parcel."""

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban import utils

from imio.urban.core.testing import IntegrationTestCase

from plone.app.testing import login
from plone import api

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

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

    def test_parcel_workflow(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        self.assertEqual(wf_tool.getChainForPortalType('Parcel'), ('one_state_workflow',))


class TestParcel(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban
        self.parcellingterm = portal.urban.parcellings.objectValues()[0]
        default_user = self.layer.default_user
        login(self.portal, default_user)
        # create a test CODT_BuildLicence
        content_type = 'CODT_BuildLicence'
        licence_folder = utils.getLicenceFolder(content_type)
        testlicence_id = 'test_{}'.format(content_type.lower())
        licence_folder.invokeFactory(content_type, id=testlicence_id)
        test_licence = getattr(licence_folder, testlicence_id)
        self.licence = test_licence
        transaction.commit()

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            api.content.delete(self.licence)
        transaction.commit()

    def test_parcels_unindexed_from_catalog(self):
        catalog = api.portal.get_tool('portal_catalog')
        licence = self.licence
        parcel = api.content.create(
            container=licence, type='Parcel', id='parcel',
            division='A', section='B', radical='6', exposant='D'
        )
        parcel_brains = catalog(UID=parcel.UID())
        self.assertEqual(len(parcel_brains), 0)

    def test_parcel_indexing_on_licence(self):
        self._test_parcel_indexing_on_container(self.licence)

    def test_parcel_indexing_on_parcellingTerm(self):
        self._test_parcel_indexing_on_container(self.parcellingterm)

    def _test_parcel_indexing_on_container(self, container):
        catalog = api.portal.get_tool('portal_catalog')
        container_id = container.id
        container_brain = catalog(id=container_id)[0]
        # so far, the index should be empty as  this container contains no parcel
        self.assertFalse(container_brain.parcelInfosIndex)

        # add a parcel1, the index should now contain this parcel reference
        parcel_1 = api.content.create(
            container=container, type='Parcel', id='parcel1',
            division='A', section='B', radical='6', exposant='D'
        )
        container_brain = catalog(id=container_id)[0]
        self.assertIn(parcel_1.get_capakey(), container_brain.parcelInfosIndex)

        # add a parcel2, the index should now contain the two parcel references
        parcel_2 = api.content.create(
            container=container, type='Parcel', id='parcel2',
            division='AA', section='B', radical='69', exposant='E'
        )
        container_brain = catalog(id=container_id)[0]
        self.assertIn(parcel_1.get_capakey(), container_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), container_brain.parcelInfosIndex)

        # we remove parcel1, parcel2 capakey should be the only remaining
        # on the index
        api.content.delete(parcel_1)
        container_brain = catalog(id=container_id)[0]
        self.assertNotIn(parcel_1.get_capakey(), container_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), container_brain.parcelInfosIndex)

        # modify parcel2 capakey, the index should be updated on the container
        old_capakey = parcel_2.get_capakey()
        parcel_2.puissance = '69'
        self.assertNotEqual(old_capakey, parcel_2.get_capakey())
        notify(ObjectModifiedEvent(parcel_2))
        container_brain = catalog(id=container_id)[0]
        self.assertIn(parcel_2.get_capakey(), container_brain.parcelInfosIndex)
        # remove parcel_2 to not impact other tests
        api.content.delete(parcel_2)

    def test_parcel_event_set_authenticity(self):
        licence = self.licence
        parcel = api.content.create(
            container=licence, type='Parcel', id='parcel1',
            division='A', section='B', radical='6', exposant='D'
        )
        # isOfficialParcel should be False
        self.assertEqual(parcel.isOfficialParcel, False)

    def test_parcel_redirectsview(self):
        licence = self.licence
        parcel = api.content.create(
            container=licence, type='Parcel', id='parcel1',
            division='A', section='B', radical='6', exposant='D'
        )
        parcel_view = parcel.restrictedTraverse('view')
        view_result = parcel_view()
        # default parcel view should redirects to the parent container
        self.assertEqual(view_result, licence.absolute_url())

    def test_divisionCode_field(self):
        licence = self.licence
        parcel = api.content.create(
            container=licence, type='Parcel', id='parcel1',
            division='69696', section='B', radical='6', exposant='D'
        )
        # divisionCode should always return the value contained in the field division.
        self.assertEqual(parcel.getDivisionCode(), parcel.getDivision())
        self.assertEqual(parcel.divisionCode, parcel.getDivision())

    def test_parcellingTerm_title_update(self):
        parcelling = self.parcellingterm
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005)')
        # after adding a parcel1, title should be updated with the base
        # references  of this parcel (here:  A, B, C but not D)
        api.content.create(container=parcelling, type='Parcel', id='parcel1', division='A', section='B', radical='6', exposant='D')
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005 - "A B 6")')

        # after adding a parcel2 with the same base refs, the title
        # should not change
        api.content.create(container=parcelling, type='Parcel', id='parcel2', division='A', section='B', radical='6', exposant='E')
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005 - "A B 6")')

        # after adding a parcel3 with different base refs, the title
        # should be updated
        parcel_3 = api.content.create(container=parcelling, type='Parcel', id='parcel3', division='AA', section='BB', radical='69', exposant='D')
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005 - "AA BB 69", "A B 6")')

        # we remove parcel1 and parcel2, title should change to only
        # keep the base refs of parcel3
        parcelling.manage_delObjects(['parcel1', 'parcel2'])
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005 - "AA BB 69")')

        # modify parcel3, parcelling title should be updated
        parcel_3.division = 'AAA'
        notify(ObjectModifiedEvent(parcel_3))
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005 - "AAA BB 69")')
