from collections import defaultdict
from contextlib import contextmanager
import cq.exceptions
import inspect


handlers_registry = defaultdict(set)


def register_handler(aggregate_type, event_name):
    def wrap(handler):
        check_handler_signature(handler)
        handlers_registry[(aggregate_type, event_name)].add(handler)
        return handler

    return wrap


def check_handler_signature(handler):
    signature = inspect.signature(handler)
    params = list(signature.parameters.keys())
    if params != ['event', 'replaying_events']:
        msg = "Handlers must accept 'event' and 'replaying_events' (%s does not)" % handler
        print(" params: %s" % str(params))
        raise cq.exceptions.ImproperlyConfigured(msg)


def handle_event(event, replaying_events):
    for handler in get_handlers(event):
        handler(event=event, replaying_events=replaying_events)


def get_handlers(event):
    return handlers_registry[(event.aggregate_type, event.name)]


@contextmanager
def side_effect():
    yield
