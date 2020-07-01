# -*- coding: utf-8 -*-
"""Setup/installation tests for Parcel."""

from imio.urban.core.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urban.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.types_tool = api.portal.get_tool('portal_types')

    def test_Parcel_type_registered(self):
        """Test if Parcel type is registered in portal_types """
        self.assertTrue(self.types_tool.get('Parcel'))
