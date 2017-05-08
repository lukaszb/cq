from marshmallow import Schema, fields

__all__ = ['register_schema', 'Schema', 'fields']


def register_schema(aggregate_class, event_name):

    def outer(method):
        if not hasattr(aggregate_class, 'schemas'):
            aggregate_class.schemas = {}

        if event_name in aggregate_class.schemas:
            msg = "Schema for action %s is already registered for %s" % (event_name, aggregate_class)
            raise RuntimeError(msg)
        else:
            aggregate_class.schemas[event_name] = method
        return method

    return outer
