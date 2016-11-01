from .entities import Action
from collections import defaultdict


handlers_registry = defaultdict(set)


def register_handler(entity_action):
    if isinstance(entity_action, Action):
        entity_action = str(entity_action)

    def wrap(handler):
        handlers_registry[entity_action].add(handler)

        def inner(event, entity):
            return
        return handler

    return wrap


def publish(event):
    for handler in get_handlers(event):
        handler(event)


def get_handlers(event):
    return handlers_registry[event.get_entity_action()]
