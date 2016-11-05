from ses.entities import Repository
from ses import exceptions
from ses import genuuid
from ses import settings


class EventSourcingApplication:
    storage_class = None
    storage_kwargs = {}

    def __init__(self):
        self.storage = self.get_storage()

    def get_storage(self):
        storage_class = self.get_storage_class()
        storage_kwargs = self.get_storage_kwargs()
        return storage_class(**storage_kwargs)

    def get_storage_class(self):
        if self.storage_class is None:
            if settings.DEFAULT_STORAGE_CLASS:
                return settings.DEFAULT_STORAGE_CLASS
            msg = "either storage_class must be set or override get_storage method"
            raise exceptions.ImproperlyConfigured(msg)
        return self.storage_class

    def get_storage_kwargs(self):
        return self.storage_kwargs

    def genuuid(self):
        return genuuid.genuuid()

    def get_repo_for_entity(self, entity_class):
        name = '%sRepository' % entity_class
        repo_class = type(name, (Repository,), {'entity_class': entity_class})
        return repo_class(storage=self.storage)
