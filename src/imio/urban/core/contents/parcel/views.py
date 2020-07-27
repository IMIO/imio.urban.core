# -*- coding: utf-8 -*-

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view


class ParcelAddForm(add.DefaultAddForm):
    """
    Parcel custom Add form.
    """

    portal_type = 'Parcel'

    def __init__(self, context, request):
        super(ParcelAddForm, self).__init__(context, request)
        # disable portlets on parcels
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)


class ParcelAddView(add.DefaultAddView):
    """
    Parcel custom Add view.
    """
    form = ParcelAddForm


class ParcelEditForm(edit.DefaultEditForm):
    """
    Parcel custom Edit form.
    """

    def __init__(self, context, request):
        super(ParcelEditForm, self).__init__(context, request)
        # disable portlets on parcels
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)


class ParcelView(view.DefaultView):
    """
    Parcel display view to be called with an overlay in parcel listings.
    """

    def __init__(self, context, request):
        super(ParcelView, self).__init__(context, request)
        # disable portlets on parcels
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)


class ParcelViewRedirects(view.DefaultView):
    """
    Parcel default view redirects to the parent container.
    """

    def __call__(self):
        return self.context.REQUEST.RESPONSE.redirect(
            self.context.aq_parent.absolute_url()
        )
