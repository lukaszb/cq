from ses.entities import Repository
from ses import exceptions
from ses import settings
import uuid


class EventSourcingApplication:
    storage_class = None

    def __init__(self):
        self.storage = self.get_storage()

    def get_storage(self):
        storage_class = self.get_storage_class()
        return storage_class()

    def get_storage_class(self):
        if self.storage_class is None:
            if settings.DEFAULT_STORAGE_CLASS:
                return settings.DEFAULT_STORAGE_CLASS
            msg = "either storage_class must be set or override get_storage method"
            raise exceptions.ImproperlyConfigured(msg)
        return self.storage_class

    def gen_uuid(self):
        return uuid.uuid4().hex

    def get_repo_for_entity(self, entity_class):
        name = '%sRepository' % entity_class
        repo_class = type(name, (Repository,), {'entity_class': entity_class})
        return repo_class(storage=self.storage)
