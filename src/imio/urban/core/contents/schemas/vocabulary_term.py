# -*- coding: utf-8 -*-

from imio.urban.core import _
from imio.urban.core.contents.utils import get_fields

from plone import api

from Products.urban.interfaces import IUrbanConfigurationValue

from zope import schema


class IVocabularyTerm(IUrbanConfigurationValue):
    """
    Urban VocabularyTerm schema.
    """
    isDefaultValue = schema.Bool(
        title=_(u'isDefaultValue'),
        default=False,
        required=False,
    )


class VocabularyTerm(object):
    """
    Base class for VocabularyTerm.
    """

    def to_dict(self):
        dict_ = {
            'id': self.id,
            'UID': self.UID(),
            'enabled': api.content.get_state(self) == 'enabled',
            'portal_type': self.portal_type,
            'title': self.title,
            'isDefaultValue': self.isDefaultValue
        }
        for field_name, field in get_fields(self):
            val = getattr(self, field_name)
            if val is None:
                val = u''
            if type(val) is str:
                val = val.decode('utf8')
            dict_[field_name] = val
        return dict_

    def __str__(self):
        if type(self.title) is unicode:
            return self.title.encode('utf-8')
        return self.title

    def __unicode__(self):
        return self.__str__().decode('utf-8')
