# -*- coding: utf-8 -*-

from Acquisition import aq_base

from imio.urban.core.testing import IntegrationTestCase

from plone import api
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES

from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

import unittest


class TestInstall(IntegrationTestCase):
    """Test installation of OpinionEventConfig."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.types_tool = api.portal.get_tool('portal_types')

    def test_OpinionEventConfig_type_registered(self):
        """Test if OpinionEventConfig type is registered in portal_types """
        self.assertTrue(self.types_tool.get('OpinionEventConfig'))

    def test_parcelling_workflow(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        self.assertEqual(wf_tool.getChainForPortalType('OpinionEventConfig'), ('activation_workflow',))


class TestUrbanEventTypes(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        login(portal, 'urbaneditor')
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        self.catalog = api.portal.get_tool('portal_catalog')
        buildlicence_brains = self.catalog(portal_type='BuildLicence', Title='Exemple Permis Urbanisme')
        self.licence = buildlicence_brains[0].getObject()
        self.event_configs = self.portal_urban.buildlicence.eventconfigs

    def testNewOpinioneventtypeAppearsInFieldVocabulary(self):
        """
        when adding a new OpinionEventConfig, its extraValue should be
        used as the display value in the vocabulary of solicitOpinions field
        of buildlicences
        """
        tool = api.portal.get_tool('portal_urban')
        eventconfigs_folder = tool.buildlicence.eventconfigs

        with api.env.adopt_roles(['Manager']):
            term_id = eventconfigs_folder.invokeFactory('OpinionEventConfig', id='voodoo', title="Demande d'avis (Vood00)", abbreviation='Vood00')
            voc_cache = tool.restrictedTraverse('urban_vocabulary_cache')
            voc_cache.update_procedure_all_vocabulary_cache(tool.buildlicence)
        term = getattr(tool.buildlicence.eventconfigs, term_id)
        expected_voc_term = (term_id, term.abbreviation)

        solicitOpinions_field = self.licence.getField('solicitOpinionsTo')
        field_voc = solicitOpinions_field.vocabulary.getDisplayList(self.licence)

        self.assertIn(expected_voc_term, field_voc.items())

    def testInquiryWithOpinionRequestIsLinkedToItsUrbanEventOpinionRequest(self):
        """
        if there is an inquiry with an opinion request and that its corresponding UrbanEventOpinionRequest
        is added, a link should be created between this inquiry and this UrbanEventOpinionRequest
        """

        licence = self.licence
        UrbanEventOpinionRequest = None
        for content in licence.objectValues():
            if content.portal_type == 'UrbanEventOpinionRequest':
                UrbanEventOpinionRequest = content
                aq_base(UrbanEventOpinionRequest)._at_creation_flag = True
                break
        notify(ObjectCreatedEvent(UrbanEventOpinionRequest))
        self.failUnless(licence.getLinkedUrbanEventOpinionRequest('belgacom') == UrbanEventOpinionRequest)
