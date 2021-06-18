# -*- coding: utf-8 -*-

from imio.urban.core.tests.helpers import BrowserTestCase

from plone.testing.z2 import Browser

from Products.urban.testing import URBAN_TESTS_CONFIG


class TestActionsDisplayiInUrbanConfig(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_urban = self.portal.portal_urban
        self.browser = Browser(self.portal)
        default_admin_user = self.layer.default_admin_user
        default_admin_password = self.layer.default_admin_password
        self.browserLogin(default_admin_user, default_admin_password)

    def test_add_POD_template_visible_on_EventConfig(self):
        event_config = self.portal_urban.buildlicence.eventconfigs.objectValues()[0]
        self.browser.open(event_config.absolute_url())
        contents = self.browser.contents
        self.assertIn('Ajout d\'un élément', contents, msg='add POD template action is not visible')
        self.assertIn('Modèle de document Urban</option>', contents, msg='add POD template action is not visible')
