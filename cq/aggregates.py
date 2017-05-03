import cq.events
from cq.events import upcaster


__all__ = ['upcaster', 'Aggregate', 'Repository', 'register_mutator']


class Aggregate:

    def __init__(self, id):
        self.id = id
        self.version = 0

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id)

    def mutate(self, event):
        mutator = self.get_mutator(event.name)
        mutator(self, event, event.data)
        self.version += 1

    def get_mutator(self, name):
        try:
            return self.__class__.mutators[name]
        except KeyError:
            msg = '%s has no mutator function registered for event type %r. ' % (self, name)
            msg += 'Please register method using @aggregates.register_mutator decorator. '
            registered_actions = ', '.join(repr(a) for a in self.__class__.mutators)
            msg += 'Currently registered actions: %s' % (registered_actions or '-')
            raise NotImplementedError(msg)

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_upcasters(cls):
        return getattr(cls, 'upcasters', [])


def register_mutator(aggregate_class, event_name):

    def outer(method):
        if not hasattr(aggregate_class, 'mutators'):
            aggregate_class.mutators = {}

        if event_name in aggregate_class.mutators:
            msg = "Mutator for action %s is already registered for %s" % (event_name, aggregate_class)
            raise RuntimeError(msg)
        else:
            aggregate_class.mutators[event_name] = method
        return method

    return outer


class Repository:
    aggregate_name = None
    aggregate_class = None

    class DoesNotExist(Exception):
        pass

    class DuplicateAggregateError(Exception):
        pass

    def __init__(self, storage):
        self.storage = storage
        if self.aggregate_class is None:
            msg = "Repository must define aggregate. Please set %s.aggregate to Aggregate subclass"
            raise RuntimeError(msg % self)

    def store(self, name, aggregate_id, data=None, revision=1):
        event = self.storage.store(
            aggregate_type=self.aggregate_class.get_name(),
            name=name,
            aggregate_id=aggregate_id,
            data=data,
            revision=revision,
        )
        event = self.upcast_event(event)
        # this way whenever we store an event it would already be upcasted for a handler
        return event

    def upcast_event(self, event):
        upcasters = self.aggregate_class.get_upcasters()
        event = cq.events.upcast(event, upcasters)
        return event

    def get_events(self, aggregate_id):
        events = self.storage.get_events(self.get_aggregate_name(), aggregate_id)
        return [self.upcast_event(event) for event in events]

    def get_aggregate(self, aggregate_id):
        aggregate = self.aggregate_class(aggregate_id)
        for event in self.get_events(aggregate_id):
            aggregate.mutate(event)
        return aggregate

    def get_aggregate_name(self):
        if self.aggregate_name:
            return self.aggregate_name
        return self.aggregate_class.get_name()
