# -*- coding: utf-8 -*-

from imio.urban.core.testing import IntegrationTestCase
from imio.urban.core.contents.schemas.vocabulary_term import VocabularyTerm


class TestVocabularyTerm(IntegrationTestCase):
    """
    """

    def test_vocabularyterm__str__(self):
        vocterm = VocabularyTerm()
        expected = 'Yolo'
        vocterm.title = expected
        msg = 'vocterms __str__ should return their title: {} != {}'
        self.assertEquals(str(vocterm), expected, msg.format(str(vocterm), expected))

    def test_vocabularyterm__unicode__(self):
        vocterm = VocabularyTerm()
        vocterm.title = 'Yoléà'
        expected = u'Yoléà'
        msg = u'vocterms __unicode__ should return their title: {} != {}'
        self.assertEquals(unicode(vocterm), expected, msg.format(unicode(vocterm), expected))
