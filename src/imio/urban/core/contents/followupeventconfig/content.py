# -*- coding: utf-8 -*-

from imio.urban.core.contents.eventconfig import EventConfig
from imio.urban.core.contents.eventconfig import IEventConfig
from imio.urban.core.contents.schemas import IVocabularyTerm
from imio.urban.core.contents.schemas import VocabularyTerm

from plone.dexterity.schema import DexteritySchemaPolicy

from zope.interface import implementer

import logging
logger = logging.getLogger('imio.urban.core: FollowUpEventConfig')


class IFollowUpEventConfig(IEventConfig):
    """
    FollowUpEventConfig zope schema.
    """


class FollowUpEventConfigSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IFollowUpEventConfig, IVocabularyTerm)


@implementer(IFollowUpEventConfig)
class FollowUpEventConfig(EventConfig, VocabularyTerm):
    """
    FollowUpEventConfig class
    """

    def mayAddFollowUpEvent(self, licence):
        """
        """
        may_add = licence.mayAddFollowUpEvent(self.id)
        return may_add
