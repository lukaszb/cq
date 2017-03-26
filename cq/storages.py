from .exceptions import SesError
from .events import Event
from .genuuid import genuuid
from .handlers import publish
from collections import defaultdict
from collections import namedtuple


UniqueItem = namedtuple('UniqueItem', '')


class Storage:
    class DuplicatedItemError(SesError):
        pass

    class DoesNotExist(SesError):
        pass

    def store(self, name, aggregate_id, data=None, ts=None):
        event = self.create_event(
            id=genuuid(),
            name=name,
            aggregate_id=aggregate_id,
            data=data,
            ts=ts,
        )
        self.append(event)
        publish(event)
        return event

    def create_event(self, id, name, aggregate_id, data=None, ts=None):
        return Event(
            id=id,
            name=name,
            aggregate_id=aggregate_id,
            data=data,
            ts=ts,
        )

    def append(self, event):
        raise NotImplementedError

    def get_events(self, name, aggregate_id):
        raise NotImplementedError

    def book_unique(self, namespace, value, aggregate_id=None):
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

    def get_events(self, aggregate_type, aggregate_id):
        return [e for e in self.events if e.aggregate_id == aggregate_id
                and e.name.startswith(aggregate_type)]

    def book_unique(self, namespace, value, aggregate_id=None):
        if value in self.uniques[namespace]:
            raise Storage.DuplicatedItemError('%s:%s already exists' % (namespace, value))
        else:
            self.uniques[namespace][value] = aggregate_id

    def get_unique(self, namespace, value):
        if value in self.uniques[namespace]:
            return self.uniques[namespace][value]
        else:
            raise self.DoesNotExist('%s:%s was not set' % (namespace, value))

    def has_unique(self, namespace, value):
        return value in self.uniques[namespace]
