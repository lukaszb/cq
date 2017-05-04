from . import exceptions
from . import genuuid
from . import settings
from .aggregates import Repository
from .events import upcaster


__all__ = ['BaseApp', 'command', 'query', 'upcaster']


def command(method):
    method.is_command = True
    return method


def query(method):
    method.is_query = True
    return method


class BaseApp:
    storage_class = None
    storage_kwargs = {}
    repos = {}

    def __init__(self):
        self.storage = self.get_storage()
        self.create_repos()

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

    def get_commands(self):
        objects = (getattr(self, attr) for attr in dir(self))
        return [obj for obj in objects if getattr(obj, 'is_command', False)]

    def get_queries(self):
        objects = (getattr(self, attr) for attr in dir(self))
        return [obj for obj in objects if getattr(obj, 'is_query', False)]

    def create_repos(self):
        for repo_name, aggregate in self.repos.items():
            repo = self.get_repo_for_aggregate(aggregate)
            setattr(self, repo_name, repo)
