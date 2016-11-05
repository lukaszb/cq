from collections import defaultdict
from collections import namedtuple
from ses.exceptions import SesError
from ses.events import Event
from ses.genuuid import genuuid
from ses.handlers import publish


UniqueItem = namedtuple('UniqueItem', '')


class Storage:
    class DuplicatedItemError(SesError):
        pass

    class DoesNotExist(SesError):
        pass

    def store(self, name, entity_id, data=None, ts=None):
        event = self.create_event(
            name=name,
            entity_id=entity_id,
            data=data,
            ts=ts,
        )
        self.append(event)
        publish(event)
        return event

    def create_event(self, name, entity_id, data=None, ts=None):
        return Event(
            name=name,
            entity_id=entity_id,
            data=data,
            ts=ts,
        )

    def append(self, event):
        raise NotImplementedError

    def get_events(self, entity_id):
        raise NotImplementedError

    def book_unique(self, namespace, value, entity_id=None):
        raise NotImplementedError

    def get_unique(self, namespace, value):
        raise NotImplementedError

    def has_unique(self, namespace, value):
        raise NotImplementedError


class LocalMemoryStorage(Storage):

    def __init__(self):
        self.events = []
        self.uniques = defaultdict(dict)

    def append(self, event):
        self.events.append(event)
        return event

    def get_events(self, entity_id):
        return [e for e in self.events if e.entity_id == entity_id]

    def book_unique(self, namespace, value, entity_id=None):
        if value in self.uniques[namespace]:
            raise Storage.DuplicatedItemError('%s:%s already exists' % (namespace, value))
        else:
            self.uniques[namespace][value] = entity_id

    def get_unique(self, namespace, value):
        if value in self.uniques[namespace]:
            return self.uniques[namespace][value]
        else:
            raise self.DoesNotExist('%s:%s was not set' % (namespace, value))

    def has_unique(self, namespace, value):
        return value in self.uniques[namespace]
