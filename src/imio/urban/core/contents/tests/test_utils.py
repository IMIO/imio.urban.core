# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase


class TestUtils(IntegrationTestCase):
    """
    """

    def test_get_portal_type_class(self):
        from imio.urban.core.contents.utils import get_portal_type_class
        from Products.ATContentTypes.content.document import ATDocument
        from Products.ATContentTypes.content.folder import ATFolder
        from imio.urban.core.contents.eventconfig import EventConfig
        # AT case
        self.assertEquals(get_portal_type_class('Document'), ATDocument)
        self.assertEquals(get_portal_type_class('Folder'), ATFolder)
        # DX case
        self.assertEquals(get_portal_type_class('EventConfig'), EventConfig)
