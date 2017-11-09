from .exceptions import SesError
from .events import Event
from .genuuid import genuuid
from .handlers import handle_event
from collections import defaultdict
from collections import namedtuple
import cq.events


UniqueItem = namedtuple('UniqueItem', '')


class Storage:
    class DuplicatedItemError(SesError):
        pass

    class DoesNotExist(SesError):
        pass

    def store(self, aggregate_type, name, aggregate_id, data=None, ts=None, revision=1):
        event = self.create_event(
            id=genuuid(),
            aggregate_type=aggregate_type,
            name=name,
            aggregate_id=aggregate_id,
            data=data,
            ts=ts,
            revision=revision,
        )
        event = self.append(event)
        handle_event(event, replaying_events=False)
        return event

    def create_event(self, id, aggregate_type, name, aggregate_id, data=None, ts=None, revision=1):
        return Event(
            id=id,
            aggregate_type=aggregate_type,
            name=name,
            aggregate_id=aggregate_id,
            data=data,
            ts=ts,
            revision=revision,
        )

    def append(self, event):
        raise NotImplementedError

    def iter_all_events(self):
        raise NotImplementedError

    def get_events(self, name, aggregate_id):
        raise NotImplementedError

    def book_unique(self, namespace, value, aggregate_id=None):
        raise NotImplementedError

    def get_unique(self, namespace, value):
        raise NotImplementedError

    def has_unique(self, namespace, value):
        raise NotImplementedError

    def replay_events(self, upcasters=None):
        for event in self.gen_replay_events(upcasters=upcasters):
            pass

    def gen_replay_events(self, upcasters=None):
        upcasters = upcasters or []
        events = self.iter_all_events()
        events = (cq.events.upcast(event, upcasters) for event in events)
        for event in events:
            self.replay_event(event)
            yield event

    def replay_event(self, event):
        handle_event(event, replaying_events=True)


class LocalMemoryStorage(Storage):

    def __init__(self):
        self.events = []
        self.uniques = defaultdict(dict)

    def append(self, event):
        self.events.append(event)
        return event

    def iter_all_events(self):
        return (e for e in self.events)

    def get_events(self, aggregate_type, aggregate_id):
        return [e for e in self.events
                if e.aggregate_id == aggregate_id and e.aggregate_type == aggregate_type]

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
