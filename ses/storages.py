from ses.exceptions import SesError
from ses.handlers import publish


class Storage:
    class DuplicatedItemError(SesError):
        pass

    class DoesNotExist(SesError):
        pass

    def store(self, entity, action, entity_id, data=None):
        event = self.append(entity, action, entity_id, data)
        publish(event)
        return event

    def append(self, entity, action, entity_id, data=None):
        raise NotImplementedError

    def get_events(self, entity_id):
        raise NotImplementedError

    def book_unique(self, namespace, value, entity_id=None):
        raise NotImplementedError

    def get_unique(self, namespace, value):
        raise NotImplementedError

    def has_unique(self, namespace, value):
        raise NotImplementedError


from collections import defaultdict
from collections import namedtuple


Event = namedtuple('Event', 'entity,action,entity_id,data')
UniqueItem = namedtuple('UniqueItem', '')


class LocalMemoryStorage(Storage):

    def __init__(self):
        self.events = []
        self.uniques = defaultdict(dict)

    def append(self, entity, action, entity_id, data=None):
        event = Event(
            entity=entity,
            action=action,
            entity_id=entity_id,
            data=data,
        )
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
