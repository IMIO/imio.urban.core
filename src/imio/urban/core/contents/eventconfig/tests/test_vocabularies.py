# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase
from imio.urban.core.contents.utils import get_portal_type_class

from plone import api

from Products.urban.testing import URBAN_TESTS_CONFIG

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


class TestInstall(IntegrationTestCase):
    """Test registered vocabularies."""

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_event_portaltypes_vocabulary(self):
        """Should return all the portal inheriting from UrbanEvent """
        vocabulary = queryUtility(IVocabularyFactory, 'urban.vocabularies.event_portaltypes')
        self.assertTrue(vocabulary)
        voc = vocabulary(self.portal)
        # when called out of any licenceConfig, should return all UrbanEvent
        # portal types
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInquiry',
            'UrbanEventAnnouncement',
            'UrbanEventInspectionReport',
            'UrbanEventFollowUp',
            'UrbanEventOpinionRequest',
            'UrbanEventMayor',
            'UrbanEventNotificationCollege',
            'UrbanEventCollege',
        ])
        self.assertEqual(set(voc.by_value), expected_types)
        # when called on a licenceConfig should only return the types in
        # the allowed contenttypes of the licence
        voc = vocabulary(self.portal.portal_urban.codt_buildlicence.eventconfigs)
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInquiry',
            'UrbanEventAnnouncement',
            'UrbanEventOpinionRequest',
            'UrbanEventNotificationCollege',
            'UrbanEventCollege',
        ])
        self.assertEqual(set(voc.by_value), expected_types)

        voc = vocabulary(self.portal.portal_urban.buildlicence.eventconfigs)
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInquiry',
            'UrbanEventOpinionRequest',
            'UrbanEventNotificationCollege',
            'UrbanEventCollege',
        ])
        self.assertEqual(set(voc.by_value), expected_types)

        voc = vocabulary(self.portal.portal_urban.envclassone.eventconfigs)
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInquiry',
            'UrbanEventOpinionRequest',
            'UrbanEventMayor',
            'UrbanEventCollege',
        ])
        self.assertEqual(set(voc.by_value), expected_types)

        voc = vocabulary(self.portal.portal_urban.inspection.eventconfigs)
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInspectionReport',
            'UrbanEventFollowUp',
        ])
        self.assertEqual(set(voc.by_value), expected_types)

    def test_event_optionalfields_vocabulary(self):
        """
        Should return all the fields from the class selected
        in eventPortalType field.
        """
        vocabulary = queryUtility(IVocabularyFactory, 'urban.vocabularies.event_optionalfields')
        self.assertTrue(vocabulary)
        voc = vocabulary(self.portal)

        # when called out of any EventConfig, should return all UrbanEvent
        # optional fields
        klass = get_portal_type_class('UrbanEvent')
        fields = [f.getName() for f in klass.schema.fields() if getattr(f, 'optional', False)]
        expected_fields = set(fields)
        self.assertEqual(set(voc.by_value.keys()), expected_fields)

        # when called on EventConfig, should return the optional fields
        # of the portal_type found on the field 'eventPortalType'
        portal_urban = api.portal.get_tool('portal_urban')
        eventconfigs = portal_urban.buildlicence.getEventConfigs()
        inquiry_config = [cfg for cfg in eventconfigs if cfg.getEventPortalType() == 'UrbanEventInquiry'][0]
        voc = vocabulary(inquiry_config)
        # the voc should be different than the optional fields of UrbanEvent
        self.assertNotEqual(set(voc.by_value.keys()), expected_fields)

        klass = get_portal_type_class(inquiry_config.getEventPortalType())
        fields = [f.getName() for f in klass.schema.fields() if getattr(f, 'optional', False)]
        expected_fields = set(fields)
        # the voc should be equal to the optional fields of UrbanEventInquiry
        self.assertEqual(set(voc.by_value.keys()), expected_fields)

    def test_event_keydates_vocabulary(self):
        """
        Should return the field eventDate + all the date fields selected
        in the eventConfig field 'activatedFields'.
        """
        vocabulary = queryUtility(IVocabularyFactory, 'urban.vocabularies.event_enabled_dates')
        self.assertTrue(vocabulary)

        portal_urban = api.portal.get_tool('portal_urban')
        eventconfig = portal_urban.buildlicence.getEventConfigs()[0]
        voc = vocabulary(eventconfig)
        # 'eventDate' should at minimum always be included
        expected_fields = set(('eventDate',))
        self.assertEqual(len(eventconfig.getActivatedFields()), 0)
        voc = vocabulary(eventconfig)
        self.assertEqual(set(voc.by_value.keys()), expected_fields)

        # enable 2 text fields and one date field
        eventconfig.activatedFields = ('depositType', 'transmitDate', 'receivedDocumentReference')
        # only the date field is expected to be included in the vocabulary
        expected_fields = set(('eventDate', 'transmitDate'))
        voc = vocabulary(eventconfig)
        self.assertEqual(set(voc.by_value.keys()), expected_fields)

    def test_event_defauttextfield_vocabulary(self):
        """
        Should return all the text fields of the portal_type selected in
        the EventConfig eventPortalType field'.
        """
        vocabulary = queryUtility(IVocabularyFactory, 'urban.vocabularies.event_text_fields')
        self.assertTrue(vocabulary)
        voc = vocabulary(self.portal)

        # when called out of any EventConfig, should return all UrbanEvent
        # text fields
        exclude = ['rights']
        klass = get_portal_type_class('UrbanEvent')
        AT_textfield_type = 'Products.Archetypes.Field.TextField'
        fields = [f.getName() for f in klass.schema.getSchemataFields('default')
                  if f.getType() == AT_textfield_type and f.getName() not in exclude]
        expected_fields = set(fields)
        self.assertEqual(set(voc.by_value.keys()), expected_fields)

        # when called on EventConfig, should return the text fields
        # of the portal_type found on the field 'eventPortalType'
        portal_urban = api.portal.get_tool('portal_urban')
        eventconfigs = portal_urban.buildlicence.getEventConfigs()
        inquiry_config = [cfg for cfg in eventconfigs if cfg.getEventPortalType() == 'UrbanEventInquiry'][0]
        voc = vocabulary(inquiry_config)
        # the voc should be different than the text fields of UrbanEvent
        self.assertNotEqual(set(voc.by_value.keys()), expected_fields)

        klass = get_portal_type_class(inquiry_config.getEventPortalType())
        fields = [f.getName() for f in klass.schema.getSchemataFields('default')
                  if f.getType() == AT_textfield_type and f.getName() not in exclude]
        expected_fields = set(fields)
        # the voc should be equal to the text fields of UrbanEventInquiry
        self.assertEqual(set(voc.by_value.keys()), expected_fields)
