# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IImioUrbanCoreLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRequiredValues(Interface):
    """Provide the required values rules for a content."""

    def is_enabled(data):
        """Return True if the rules must be applied."""

    def get_rules(data):
        """Return {field_name: {'all': values, 'any': [values, ...]}}."""