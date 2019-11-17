
from django.core import exceptions
from django.db.models import fields
from django.db import models
from formula import Formula


class FormulaField(fields.CharField):
    formula = None

    def __init__(self, formula=None, *args, **kwargs):
        self.formula = formula
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, tuple):
            formula, value = value 
            value = Formula(formula, value)
            value = value.value
        elif self.formula:
            value = Formula(self.formula, value)
            value = value.value
        return value