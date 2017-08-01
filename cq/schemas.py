"""
Event schema validation code.
Currently this is mostly light abstraction over `marshmallow`.
"""
from marshmallow import fields
from marshmallow import Schema as _Schema

EventSchema = _Schema

__all__ = ['EventSchema', 'fields']
