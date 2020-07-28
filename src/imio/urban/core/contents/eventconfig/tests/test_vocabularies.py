# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase

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
        ])
        self.assertEquals(set(voc.by_value), expected_types)
        # when called on a licenceConfig should only return the types in
        # the allowed contenttypes of the licence
        voc = vocabulary(self.portal.portal_urban.codt_buildlicence.urbaneventtypes)
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInquiry',
            'UrbanEventAnnouncement',
            'UrbanEventOpinionRequest',
        ])
        self.assertEquals(set(voc.by_value), expected_types)

        voc = vocabulary(self.portal.portal_urban.buildlicence.urbaneventtypes)
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInquiry',
            'UrbanEventOpinionRequest',
        ])
        self.assertEquals(set(voc.by_value), expected_types)

        voc = vocabulary(self.portal.portal_urban.inspection.urbaneventtypes)
        expected_types = set([
            'UrbanEvent',
            'UrbanEventInspectionReport',
            'UrbanEventFollowUp',
        ])
        self.assertEquals(set(voc.by_value), expected_types)
