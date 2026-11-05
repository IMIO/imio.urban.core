# -*- coding: utf-8 -*-

from imio.urban.core import _
from imio.urban.core.interfaces import IRequiredValues
from plone import api
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import safe_unicode
from z3c.form.validator import NoInputData
from zope.component import getUtility
from zope.component import queryAdapter
from zope.interface import Invalid
from zope.interface import providedBy
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.schema.interfaces import IField


def get_portal_type_class(portal_type):
    """
    Return the class of the given portal_type.
    Implemented for both AT and DX but should only keep DX once
    the urban DX migration is complete.
    """
    types_tool = api.portal.get_tool('portal_types')
    type_definition = getattr(types_tool, portal_type)
    # dexterity
    if hasattr(type_definition, 'klass'):
        klass_path = '.'.join(type_definition.klass.split('.')[:-1])
        klass_name = type_definition.klass.split('.')[-1]
        klass_module = __import__(klass_path, fromlist=[klass_name])
        klass = getattr(klass_module, klass_name)
    # Archetype, to delete later
    else:
        at_tool = api.portal.get_tool('archetype_tool')
        module = [at_def for at_def in at_tool.listRegisteredTypes()
                  if at_def['portal_type'] == type_definition.id]
        module = module or [at_def for at_def in at_tool.listRegisteredTypes()
                            if at_def['meta_type'] == type_definition.content_meta_type]
        klass = module and module[0]['klass']
    return klass


def get_fields(dx_object):
    fti = getUtility(IDexterityFTI, name=dx_object.portal_type)
    fti_schema = fti.lookupSchema()
    fields = [(n, f) for n, f in fti_schema.namesAndDescriptions(all=True)]

    # also lookup behaviors
    for behavior_id in fti.behaviors:
        behavior = getUtility(IBehavior, behavior_id).interface
        fields.extend([(n, f) for n, f in behavior.namesAndDescriptions(all=True)])

    return fields


def validate_required_values(data):
    """Entry point called from an invariant.

    The rules come from the IRequiredValues adapter of the form context,
    the adapter decides if they apply and which ones.
    """
    adapter = queryAdapter(data, IRequiredValues)
    if adapter is None or not adapter.is_enabled(data):
        return
    check_required_values(data, adapter.get_rules(data))


def check_required_values(data, rules):
    """Raise Invalid if a field does not match its rule.

    rules: {field_name: {'all': values, 'any': [values, ...]}}
           'all': every value must be present
           'any': each group needs at least one value present
           values: [{'value': value, 'label': label}, ...]
                   'label' is optional (defaults to the value) and can be
                   an i18n message, a plain value can replace the dict
    """
    request = getRequest()
    errors = []
    for field_name, rule in rules.items():
        current_values = to_unicode_set(get_field_value(data, field_name))
        field_errors = check_field_rule(rule, current_values, request)
        if field_errors:
            field_title = get_field_title(data, field_name, request)
            errors.append("{0}: {1}".format(field_title, ", ".join(field_errors)))

    if errors:
        raise Invalid(" ; ".join(errors))


def check_field_rule(rule, current_values, request):
    errors = []

    all_labels = to_labels(rule.get("all"))
    missing_labels = [
        label for value, label in all_labels.items() if value not in current_values
    ]
    if missing_labels:
        message = _(
            "missing_all_required_values",
            default="missing required values ${values}",
        )
        errors.append(build_message(message, missing_labels, request))

    for group in rule.get("any", []):
        any_labels = to_labels(group)
        if not set(any_labels) & current_values:
            message = _(
                "missing_any_required_value",
                default="at least one of ${values}",
            )
            errors.append(build_message(message, any_labels.values(), request))

    return errors


def build_message(message, labels, request):
    """Translate the message with the translated labels as ${values}."""
    values = sorted(translate(label, context=request) for label in labels)
    message = Message(message, mapping={"values": ", ".join(values)})
    return translate(message, context=request)


def get_field_title(data, field_name, request):
    """Translated field title, found in the schemas provided by data."""
    for schema in providedBy(data).flattened():
        field = schema.get(field_name)
        if IField.providedBy(field):
            return translate(field.title, context=request)
    return safe_unicode(field_name)


def to_labels(values):
    """Return {unicode value: label}, the label defaults to the value."""
    if values is None:
        return {}
    if isinstance(values, (basestring, dict)):
        values = [values]

    labels = {}
    for item in values:
        if not isinstance(item, dict):
            item = {"value": item}
        value = to_unicode(item["value"])
        labels[value] = item.get("label", value)
    return labels


def get_field_value(data, field_name):
    if isinstance(data, dict):
        return data.get(field_name)
    try:
        return getattr(data, field_name, None)
    except NoInputData:
        return None


def to_unicode_set(value):
    """Return the value(s) as a set of unicode strings."""
    if value is None:
        return set()

    is_single_value = isinstance(value, basestring) or not hasattr(value, "__iter__")
    if is_single_value:
        value = [value]

    return {to_unicode(v) for v in value}


def to_unicode(value):
    if isinstance(value, basestring):
        return safe_unicode(value)
    return unicode(value)
