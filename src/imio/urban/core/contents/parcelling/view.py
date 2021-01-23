# -*- coding: utf-8 -*-

from plone.dexterity.browser.view import DefaultView
from Products.urban.browser.table.urbantable import ParcelsTable


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
            return ''
        parceltable = ParcelsTable(self.context, self.request, values=parcels)
        parceltable.update()
        render = parceltable.render()
        return render
