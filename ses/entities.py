class EntityMetaclass(type):
    def __new__(cls, name, bases, attrs):
        newcls = super(EntityMetaclass, cls).__new__(cls, name, bases, attrs)
        for attr, val in attrs.items():
            if isinstance(val, Action):
                val.entity_class = newcls
                val.name = getattr(val, 'name') or attr

        for attr, val in attrs.items():
            if hasattr(val, 'mutator_for'):
                if str(val.mutator_for) in newcls.mutators:
                    msg = "Mutator for action %s is already registered for %s" % (val.mutator_for, newcls)
                    raise RuntimeError(msg)
                else:
                    newcls.mutators[str(val.mutator_for)] = val

        return newcls


class Action:
    entity_class = None

    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        if self.entity_class:
            return '%s.%s' % (self.entity_class.get_name(), self.name)
        else:
            return self.name

    def __eq__(self, other):
        return str(self) == str(other)


class Entity(metaclass=EntityMetaclass):
    Action = Action
    mutators = {}

    def __init__(self, id):
        self.id = id
        self.version = 1

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id)

    def mutate(self, event):
        mutator = self.get_mutator(event.get_entity_action())
        mutator(self, event.data)
        self.version += 1

    def get_mutator(self, action):
        try:
            return self.__class__.mutators[str(action)]
        except KeyError:
            msg = '%s has no mutator function registered for action %r. ' % (self, action)
            msg += 'Please register method using @entities.register_mutator decorator. '
            registered_actions = ', '.join(repr(a) for a in self.__class__.mutators)
            msg += 'Currently registered actions: %s' % (registered_actions or '-')
            raise NotImplementedError(msg)

    @classmethod
    def get_name(cls):
        return cls.__name__


def register_mutator(action):
    assert isinstance(action, Action), "register_mutator only with Entity.Action instance"
    action_key = str(action)
    action.entity_class.mutators

    def outer(method):
        if action_key in action.entity_class.mutators:
            msg = "Mutator for action %s is already registered for %s" % (action, action.entity_class)
            raise RuntimeError(msg)
        else:
            action.entity_class.mutators[action_key] = method
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

    def store(self, action, entity_id, data=None):
        if isinstance(action, Action) and '.' in str(action):
            entity_name, action = str(action).split('.', 1)
        else:
            entity_name = self.get_entity_name()
        return self.storage.store(entity_name, action, entity_id, data)

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
