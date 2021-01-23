# -*- coding: utf-8 -*-

import unittest


class BrowserTestCase(unittest.TestCase):
    """
    Base class for browser test cases.
    """

    def browserLogin(self, user, password=None):
        self.browser.handleErrors = False
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = password or user
        self.browser.getControl(name='submit').click()
