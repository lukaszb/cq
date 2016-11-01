from ses.exceptions import SesError
from ses.handlers import publish


class Storage:
    class DuplicatedItemError(SesError):
        pass

    def store(self, entity, action, entity_id, data=None):
        event = self.append(entity, action, entity_id, data)
        publish(event)
        return event

    def append(self, entity, action, entity_id, data=None):
        raise NotImplementedError

    def get_events(self, entity_id):
        raise NotImplementedError

    def book_unique(self, namespace, value):
        raise NotImplementedError
