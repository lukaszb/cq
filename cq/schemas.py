"""
Event schema validation code.
Currently this is only light abstraction over `marshmallow`.
"""
from marshmallow import fields
from marshmallow import Schema as _Schema
from marshmallow import validates_schema
from marshmallow import ValidationError


__all__ = ['EventSchema', 'fields']


class EventSchema(_Schema):
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        original_data = original_data or {}
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)
