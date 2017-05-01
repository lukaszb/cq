from .aggregates import Todo
from cq.app import BaseApp
from cq.contrib.sqlalchemy.storage import SqlAlchemyStorage


class TodoApp(BaseApp):
    storage_class = SqlAlchemyStorage
    storage_kwargs = {'db_uri': 'sqlite:///:memory:'}
    repos = {'repo': Todo}

    def add(self, name):
        uuid = self.genuuid()
        return self.repo.store('Added', uuid, data={'name': name})

    def finish(self, todo_id):
        self.repo.get_aggregate(todo_id)
        self.repo.store('Finished', todo_id)

    def reopen(self, todo_id):
        self.repo.get_aggregate(todo_id)
        self.repo.store('Reopened', todo_id)


todos = TodoApp()
