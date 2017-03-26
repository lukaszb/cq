class Aggregate:
    mutators = {}

    def __init__(self, id):
        self.id = id
        self.version = 1

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


def register_mutator(aggregate_class, event_name):

    def outer(method):
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

    def store(self, name, aggregate_id, data=None):
        return self.storage.store(name, aggregate_id, data)

    def get_events(self, aggregate_id):
        return self.storage.get_events(self.get_aggregate_name(), aggregate_id)

    def get_aggregate(self, aggregate_id):
        aggregate = self.aggregate_class(aggregate_id)
        for event in self.get_events(aggregate_id):
            aggregate.mutate(event)
        return aggregate

    def get_aggregate_name(self):
        if self.aggregate_name:
            return self.aggregate_name
        return self.aggregate_class.get_name()
