from collections import defaultdict


handlers_registry = defaultdict(set)


def register_handler(event_name):
    def wrap(handler):
        handlers_registry[event_name].add(handler)

        def inner(event, entity):
            return
        return handler

    return wrap


def publish(event):
    for handler in get_handlers(event):
        handler(event)


def get_handlers(event):
    return handlers_registry[event.name]
