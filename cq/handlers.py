from collections import defaultdict


handlers_registry = defaultdict(set)


def register_handler(aggregate_type, event_name):
    def wrap(handler):
        handlers_registry[(aggregate_type, event_name)].add(handler)

        def inner(event, aggregate):
            return
        return handler

    return wrap


def handle_event(event):
    for handler in get_handlers(event):
        handler(event)


def get_handlers(event):
    return handlers_registry[(event.aggregate_type, event.name)]
