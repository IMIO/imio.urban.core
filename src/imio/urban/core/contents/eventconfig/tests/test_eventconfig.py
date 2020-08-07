# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase

from plone import api
from plone.app.testing import login
from Products.urban.interfaces import IUrbanEvent
from Products.urban.testing import URBAN_TESTS_LICENCES

from zope.component.interface import getInterface
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


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
        For each EventConfig, at least one event should have been created and can be found
        with 'getLinkedUrbanEvents' method.
        """
        for event_config in self.event_configs.objectValues():
            linked_urbanevents = event_config.getLinkedUrbanEvents()
            if event_config.canBeCreatedInLicence(self.buildlicence):
                self.assertEqual(len(linked_urbanevents), 1)
                self.assertEqual(linked_urbanevents[0].getUrbaneventtypes(), event_config)
                self.assertTrue(IUrbanEvent.providedBy(linked_urbanevents[0]))

    def test_canBeCreatedInLicence(self):
        """
        The method canBeCreatedInLicence() should return True or False
        depending on the TALCondition field.
        """
        event_config = getattr(self.event_configs, 'rapport-du-college')
        event_config.TALCondition = 'python: False'
        self.assertFalse(event_config.canBeCreatedInLicence(self.buildlicence))
        event_config.TALCondition = 'python: True'
        self.assertTrue(event_config.canBeCreatedInLicence(self.buildlicence))

    def test_marker_interfaces_update(self):
        """
        When updating the field eventType on an EventConfig, all the existing events should be
        updated as well to add or remove the marker interfaces in the new values.
        """
        event_config = getattr(self.event_configs, 'rapport-du-college')
        event = event_config.getLinkedUrbanEvents()[0]
        inquiry_marker = 'Products.urban.interfaces.IInquiryEvent'
        inquiry_marker_interface = getInterface('', inquiry_marker)

        # for now the marker should not be provided on the event
        self.assertFalse(inquiry_marker_interface.providedBy(event))
        # set Inquiry marker and trigger modified zope event
        event_config.eventType = (inquiry_marker,)
        notify(ObjectModifiedEvent(event_config))
        # now the marker should be provided on the event
        self.assertTrue(inquiry_marker_interface.providedBy(event))
        # remove all the markers
        event_config.eventType = ()
        notify(ObjectModifiedEvent(event_config))
        # the marker should not be provided on the event anymore
        self.assertFalse(inquiry_marker_interface.providedBy(event))

    def test_keyEvent_default(self):
        catalog = self.catalog
        event_config_a = getattr(self.event_configs, 'rapport-du-college')
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # by defaut, key events are enabled, and the index in the catalog should not be empty
        self.assertEqual(event_config_a.getIsKeyEvent(), True)
        self.failUnless(buildlicence_brain.last_key_event is not None)

    def test_keyEvent_with_existing_urbanevent(self):
        catalog = self.catalog
        for event_config in self.event_configs.objectValues():
            # reset urban event types twice to make sure to trigger the reindex
            event_config.isKeyEvent = True
            notify(ObjectModifiedEvent(event_config))
            event_config.isKeyEvent = False
            notify(ObjectModifiedEvent(event_config))
        event_config_a = getattr(self.event_configs, 'rapport-du-college')
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # set 'rapport-du-college' as a key event, buildlicence index should be updated
        event_config_a.isKeyEvent = True
        notify(ObjectModifiedEvent(event_config_a))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], event_config_a.Title())

    def test_keyEvent_without_existing_urbanevent(self):
        """
        When the field LastKeyEvent is activated in an EventConfig EC of the cfg, all the licences of the
        given cfg type should have the index 'lastKeyEvent' updated to the value EC if they owns an
        UrbanEvent EC and if that UrbanEvent is the last keyEvent created in the licence.
        """
        catalog = self.catalog
        for event_config in self.event_configs.objectValues():
            # reset urban event types twice to make sure to trigger the reindex
            event_config.isKeyEvent = True
            notify(ObjectModifiedEvent(event_config))
            event_config.isKeyEvent = False
            notify(ObjectModifiedEvent(event_config))
        event_config_b = getattr(self.event_configs, 'sncb')
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # set 'belgacom' as a key event, buildlicence last_key_event index should not change
        # as the corresponding EventConfig has never been created in this buildlicence
        event_config_b.isKeyEvent = True
        notify(ObjectModifiedEvent(event_config_b))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(buildlicence_brain.last_key_event, None)

    def test_keyEvents_ordering_by_dates(self):
        """
        When the field LastKeyEvent is activated in an EventConfig EC of the cfg, all the licences of the
        given cfg type should have the index 'lastKeyEvent' updated to the value EC if they owns an
        UrbanEvent EC and if that UrbanEvent is the last keyEvent created in the licence.
        """
        catalog = self.catalog
        for event_config in self.event_configs.objectValues():
            # reset urban event types twice to make sure to trigger the reindex
            event_config.isKeyEvent = True
            notify(ObjectModifiedEvent(event_config))
            event_config.isKeyEvent = False
            notify(ObjectModifiedEvent(event_config))
        event_config_a = getattr(self.event_configs, 'rapport-du-college')
        event_config_c = getattr(self.event_configs, 'depot-de-la-demande')
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # set 'rapport-du-college' as a key event, buildlicence index should be updated
        event_config_a.isKeyEvent = True
        notify(ObjectModifiedEvent(event_config_a))
        # set 'depot-de-la-demande' as key event, buildlicence last_key_event index should not change as
        # 'rapport-du-college' is still the most recent keyEvent created
        event_config_c.isKeyEvent = True
        notify(ObjectModifiedEvent(event_config_c))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], event_config_a.Title())
        # set 'rapport-du-college' back as a normal EventConfig, buildlicence last_key_event index should be
        #  updated as 'depot-de-la-demande' becomes now the most recent key urban event created
        event_config_a.isKeyEvent = False
        notify(ObjectModifiedEvent(event_config_a))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], event_config_c.Title())
