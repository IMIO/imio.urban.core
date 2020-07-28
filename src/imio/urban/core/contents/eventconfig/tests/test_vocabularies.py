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
        import ipdb; ipdb.set_trace()
