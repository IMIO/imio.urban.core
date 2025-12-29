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

    numbering = schema.TextLine(
        title=_("Numbering"),
        description=_("Use this field to add a custom numbering that will be shown in edit forms but not on document render."),
        required=False,
        default=u""
    )

    extraValue = schema.TextLine(
        title=_("Extravalue"),
        description=_("This field is made to store extra value if needed."),
        required=False,
        default=u""
    )

    coring_id = schema.TextLine(
        title=_("CoringId"),
        description=_("This field is made to store the coring id."),
        required=False,
        default=u""
    )

    startValidity = schema.Date(
        title=_("StartValidity"),
        required=False,
        default=None
    )

    endValidity = schema.Date(
        title=_("EndValidity"),
        required=False,
        default=None
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

    def getFormattedDescription(self, linebyline=True, prefix=""):
        """
        This method can get the description in different formats
        """
        descr = self.description.raw
        # add prefix only if description isn't empty
        #    or is different from code like "<p> </p>" ??
        if descr and prefix:
            descr = prefix + descr
        if linebyline:
            return descr
        else:
            # we need to make a single string with everything we have in the HTML description
            return re.sub(r"<[^>]*?>", " ", descr).replace("  ", " ")

    def getNumbering(self):
        return self.numbering

    def getExtraValue(self):
        return self.extraValue

    def getCoring_id(self):
        return self.coring_id

    def getStartValidity(self):
        return self.startValidity

    def getEndValidity(self):
        return self.endValidity
