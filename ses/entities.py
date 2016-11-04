class Entity:
    mutators = {}

    def __init__(self, id):
        self.id = id
        self.version = 1

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id)

    def mutate(self, event):
        mutator = self.get_mutator(event.name)
        mutator(self, event.data)
        self.version += 1

    def get_mutator(self, name):
        try:
            return self.__class__.mutators[name]
        except KeyError:
            msg = '%s has no mutator function registered for event type %r. ' % (self, name)
            msg += 'Please register method using @entities.register_mutator decorator. '
            registered_actions = ', '.join(repr(a) for a in self.__class__.mutators)
            msg += 'Currently registered actions: %s' % (registered_actions or '-')
            raise NotImplementedError(msg)

    @classmethod
    def get_name(cls):
        return cls.__name__


def register_mutator(entity_class, event_name):

    def outer(method):
        if event_name in entity_class.mutators:
            msg = "Mutator for action %s is already registered for %s" % (event_name, entity_class)
            raise RuntimeError(msg)
        else:
            entity_class.mutators[event_name] = method
        return method

    return outer


class Repository:
    entity_name = None
    entity_class = None

    class DoesNotExist(Exception):
        pass

    class DuplicateEntityError(Exception):
        pass

    def __init__(self, storage):
        self.storage = storage
        if self.entity_class is None:
            msg = "Repository must define entity. Please set %s.entity to Entity subclass"
            raise RuntimeError(msg % self)

    def store(self, name, entity_id, data=None):
        return self.storage.store(name, entity_id, data)

    def get_events(self, entity_id):
        return self.storage.get_events(entity_id)

    def get_entity(self, entity_id):
        entity = self.entity_class(entity_id)
        for event in self.get_events(entity_id):
            entity.mutate(event)
        return entity

    def get_entity_name(self):
        if self.entity_name:
            return self.entity_name
        return self.entity_class.get_name()
