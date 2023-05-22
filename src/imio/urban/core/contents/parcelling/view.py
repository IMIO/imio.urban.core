# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.urban.browser.table.urbantable import (LicenceAttachmentsTable,
                                                     ParcelsTable)


class ParcellingView(DefaultView):
    """
    This manage methods of Parcelling view
    """

    def __init__(self, context, request):
        super(ParcellingView, self).__init__(context, request)
        self.context = context
        self.request = request

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ""
        parceltable = ParcelsTable(self.context, self.request, values=parcels)
        parceltable.update()
        render = parceltable.render()
        return render

    def renderListing(self, table):
        table.update()
        return table.render()

    def renderAttachmentsListing(self):
        licence = aq_inner(self.context)
        attachments = licence.objectValues("ATBlob")
        if not attachments:
            return ""
        table = LicenceAttachmentsTable(self.context, self.request, values=attachments)
        return self.renderListing(table)

    def mayAddAttachment(self):
        context = aq_inner(self.context)
        member = api.portal.get_tool("portal_membership").getAuthenticatedMember()
        if member.has_permission("ATContentTypes: Add File", context):
            return True
        return False
