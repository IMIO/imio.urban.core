# -*- coding: utf-8 -*-
"""Setup/installation tests for Parcel."""

from Products.urban import utils
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL

from imio.urban.core.testing import IntegrationTestCase

from plone import api
from plone.app.testing import login

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import transaction
import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of Parcel."""

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

    def _test_parcel_indexing_on_container(self, container):
        catalog = api.portal.get_tool('portal_catalog')
        container_id = container.id
        container_brain = catalog(id=container_id)[0]
        # so far, the index should be empty as  this container contains no parcel
        self.assertFalse(container_brain.parcelInfosIndex)

        # add a parcel1, the index should now contain this parcel reference
        parcel_1 = api.content.create(
            container=container, type='Parcel', id='parcel1',
            division=u'A', section=u'B', radical=u'6', exposant=u'D'
        )
        container_brain = catalog(id=container_id)[0]
        self.assertIn(parcel_1.get_capakey(), container_brain.parcelInfosIndex)

        # add a parcel2, the index should now contain the two parcel references
        parcel_2 = api.content.create(
            container=container, type='Parcel', id='parcel2',
            division=u'AA', section=u'B', radical=u'69', exposant=u'E'
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
        parcel_2.puissance = u'69'
        self.assertNotEqual(old_capakey, parcel_2.get_capakey())
        notify(ObjectModifiedEvent(parcel_2))
        container_brain = catalog(id=container_id)[0]
        self.assertIn(parcel_2.get_capakey(), container_brain.parcelInfosIndex)

    def test_parcel_indexing_on_boundlicences(self):
        licence = self.licence
        inspection = self._create_test_licence('Inspection')
        ticket = self._create_test_licence('Ticket')
        inspection.setBound_licences([licence])
        inspection.setUse_bound_licence_infos(True)
        notify(ObjectModifiedEvent(inspection))
        ticket.setBound_inspection(inspection)
        ticket.setUse_bound_inspection_infos(True)
        notify(ObjectModifiedEvent(ticket))
        catalog = api.portal.get_tool('portal_catalog')

        licence_brain = catalog(UID=licence.UID())[0]
        inspection_brain = catalog(UID=inspection.UID())[0]
        ticket_brain = catalog(UID=ticket.UID())[0]
        # so far, the index should be empty as  this licence contains no parcel
        self.assertFalse(licence_brain.parcelInfosIndex)
        self.assertFalse(inspection_brain.parcelInfosIndex)
        self.assertFalse(ticket_brain.parcelInfosIndex)

        # add a parcel1, the index should now contain this parcel reference
        parcel_1 = api.content.create(
            container=licence, type='Parcel', id='parcel1',
            division=u'A', section=u'B', radical=u'6', exposant=u'D'
        )
        licence_brain = catalog(UID=licence.UID())[0]
        inspection_brain = catalog(UID=inspection.UID())[0]
        ticket_brain = catalog(UID=ticket.UID())[0]
        self.assertIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_1.get_capakey(), inspection_brain.parcelInfosIndex)
        self.assertIn(parcel_1.get_capakey(), ticket_brain.parcelInfosIndex)

        # add a parcel2, the index should now contain the two parcel references
        parcel_2 = api.content.create(
            container=licence, type='Parcel', id='parcel2',
            division=u'AA', section=u'B', radical=u'69', exposant=u'E'
        )
        licence_brain = catalog(UID=licence.UID())[0]
        inspection_brain = catalog(UID=inspection.UID())[0]
        ticket_brain = catalog(UID=ticket.UID())[0]
        self.assertIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_1.get_capakey(), inspection_brain.parcelInfosIndex)
        self.assertIn(parcel_1.get_capakey(), ticket_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), inspection_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), ticket_brain.parcelInfosIndex)

        # we remove parcel1, parcel2 capakey should be the only remaining
        # on the index
        api.content.delete(parcel_1)
        licence_brain = catalog(UID=licence.UID())[0]
        inspection_brain = catalog(UID=inspection.UID())[0]
        ticket_brain = catalog(UID=ticket.UID())[0]
        self.assertNotIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertNotIn(parcel_1.get_capakey(), inspection_brain.parcelInfosIndex)
        self.assertNotIn(parcel_1.get_capakey(), ticket_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), inspection_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), ticket_brain.parcelInfosIndex)

        # modify parcel2 capakey, the index should be updated on the licence
        old_capakey = parcel_2.get_capakey()
        parcel_2.puissance = u'69'
        self.assertNotEqual(old_capakey, parcel_2.get_capakey())
        notify(ObjectModifiedEvent(parcel_2))
        licence_brain = catalog(UID=licence.UID())[0]
        inspection_brain = catalog(UID=inspection.UID())[0]
        ticket_brain = catalog(UID=ticket.UID())[0]
        self.assertIn(parcel_2.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), inspection_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), ticket_brain.parcelInfosIndex)

    def test_parcel_event_set_authenticity(self):
        licence = self.licence
        parcel = api.content.create(
            container=licence, type='Parcel', id='parcel1',
            division=u'A', section=u'B', radical=u'6', exposant=u'D'
        )
        # isOfficialParcel should be False
        self.assertEqual(parcel.isOfficialParcel, False)

    def test_parcel_redirectsview(self):
        licence = self.licence
        parcel = api.content.create(
            container=licence, type='Parcel', id='parcel1',
            division=u'A', section=u'B', radical=u'6', exposant=u'D'
        )
        parcel_view = parcel.restrictedTraverse('view')
        view_result = parcel_view()
        # default parcel view should redirects to the parent container
        self.assertEqual(view_result, licence.absolute_url())

    def test_divisionCode_field(self):
        licence = self.licence
        parcel = api.content.create(
            container=licence, type='Parcel', id='parcel1',
            division=u'69696', section=u'B', radical=u'6', exposant=u'D'
        )
        # divisionCode should always return the value contained in the field division.
        self.assertEqual(parcel.getDivisionCode(), parcel.getDivision())
        self.assertEqual(parcel.divisionCode, parcel.getDivision())
