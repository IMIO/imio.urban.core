# -*- coding: utf-8 -*-

from imio.actionspanel.browser.views import DeleteGivenUidView

from AccessControl import Unauthorized
from imio.actionspanel import ActionsPanelMessageFactory as _
from imio.actionspanel.interfaces import IContentDeletable
from imio.actionspanel.utils import unrestrictedRemoveGivenObject
from imio.helpers.content import uuidsToObjects

import transaction


class UrbanDeleteGivenUidView(DeleteGivenUidView):
    """
    Override deleteUID view to be able to delete uncatalogued objects.
    """

    def __call__(self,
                 object_uid,
                 redirect=True,
                 catch_before_delete_exception=True):
        """ """
        # redirect can by passed by jQuery, in this case, we receive '0' or '1'
        if redirect == '0':
            redirect = False
        elif redirect == '1':
            redirect = True
        # Get the object to delete, if not found using UID index,
        # try with contained_uids index
        objs = uuidsToObjects(uuids=[object_uid], check_contained_uids=True)
        if not objs:
            # URBAN ovveride: check if the context is the UID to delete.
            if self.context.UID() == object_uid:
                objs = [self.context]
            else:
                raise KeyError('The given uid could not be found!')
        obj = objs[0]

        # we use an adapter to manage if we may delete the object
        # that checks if the user has the 'Delete objects' permission
        # on the content by default but that could be overrided
        if IContentDeletable(obj).mayDelete():
            msg = {'message': _('object_deleted'),
                   'type': 'info'}
            # remove the object
            # just manage BeforeDeleteException because we rise it ourselves
            from OFS.ObjectManager import BeforeDeleteException
            try:
                unrestrictedRemoveGivenObject(obj)
            except BeforeDeleteException, exc:
                # abort because element was removed
                transaction.abort()
                msg = {'message': u'{0} ({1})'.format(
                    exc.message, exc.__class__.__name__),
                    'type': 'error'}
                if not catch_before_delete_exception:
                    raise BeforeDeleteException(exc.message)
        else:
            # as the action calling delete_givenuid is already protected by the check
            # made in the 'if' here above, if we arrive here it is that user is doing
            # something wrong, we raise Unauthorized
            raise Unauthorized

        # Redirect the user to the correct page and display the correct message.
        self.portal.plone_utils.addPortalMessage(**msg)
        if redirect and not msg['type'] == 'error':
            return self._findViewablePlace(obj)
