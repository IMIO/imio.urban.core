# -*- coding: utf-8 -*-

from imio.urban.core import _

from plone.app import textfield
from plone.dexterity.content import Item
from plone.supermodel import model

from zope import schema
from zope.interface import implementer


class IParcelling(model.Schema):
    """
    Parcelling dexterity schema.
    """

    title = schema.TextLine(
        title=_(u'urban_label_title'),
        required=False,
    )

    label = schema.TextLine(
        title=_(u'urban_label_label'),
        required=True,
    )

    subdividerName = schema.TextLine(
        title=_(u'urban_label_subdividerName'),
        required=True,
    )

    authorizationDate = schema.Date(
        title=_(u'urban_label_authorizationDate'),
        required=False,
    )

    approvalDate = schema.Date(
        title=_(u'urban_label_approvalDate'),
        required=False,
    )

    communalReference = schema.TextLine(
        title=_(u'urban_label_CommunalReference'),
        required=False,
    )

    DGO4Reference = schema.TextLine(
        title=_(u'urban_label_DGO4Reference'),
        required=False,
    )

    numberOfParcels = schema.Int(
        title=_(u'urban_label_numberOfParcels'),
        required=True,
    )

    changesDescription = textfield.RichText(
        title=_(u'urban_label_changesDescription'),
        required=False,
    )


@implementer(IParcelling)
class Parcelling(Item):
    """
    Parcelling dexterity class.
    """

    def getLabel(self):
        return self.label or ''

    def getSubdividerName(self):
        return self.subdividerName or ''

    def getAuthorizationDate(self):
        return self.authorizationDate or None

    def getApprovalDate(self):
        return self.approvalDate or None

    def getCommunalReference(self):
        return self.communalReference or ''

    def getDGO4Reference(self):
        return self.DGO4Reference or ''

    def getNumberOfParcels(self):
        return self.numberOfParcels or ''

    def getChangesDescription(self):
        return self.changesDescription or '<p></p>'

    def Title(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        title = u"%s (%s" % (self.getLabel(), self.getSubdividerName())

        auth_date = self.getAuthorizationDate()
        if auth_date:
            title = u'%s - %s' % (title, auth_date.strftime('%d/%m/%Y'))

        approval_date = self.getApprovalDate()
        if approval_date:
            title = u'%s - %s' % (title, approval_date.strftime('%d/%m/%Y'))

        title = u'%s)' % title
        return title
