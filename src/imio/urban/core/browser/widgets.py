# -*- coding: utf-8 -*-

from datetime import date

from plone.formwidget.datetime.z3cform.widget import DateWidget

from z3c.form.widget import FieldWidget


class UrbanDateWidget(DateWidget):
    """
    Override default plone date widget to ensure the starting year
    is always at least 1960.
    """
    years_range = (1960 - date.today().year, 10)


def UrbanDateFieldWidget(field, request):
    return FieldWidget(field, UrbanDateWidget(request))
