from . import exceptions
from . import genuuid
from . import settings
from .aggregates import Repository


class BaseApp:
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

    def get_repo_for_aggregate(self, aggregate_class):
        name = '%sRepository' % aggregate_class
        repo_class = type(name, (Repository,), {'aggregate_class': aggregate_class})
        return repo_class(storage=self.storage)
