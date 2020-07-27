# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urban.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if imio.urban.core is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('imio.urban.core'))

    def test_uninstall(self):
        """Test if imio.urban.core is cleanly uninstalled."""
        self.installer.uninstallProducts(['imio.urban.core'])
        self.assertFalse(self.installer.isProductInstalled('imio.urban.core'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IImioUrbanCoreLayer is registered."""
        from imio.urban.core.interfaces import IImioUrbanCoreLayer
        from plone.browserlayer import utils
        self.assertIn(IImioUrbanCoreLayer, utils.registered_layers())
