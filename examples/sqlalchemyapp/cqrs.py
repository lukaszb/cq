from .entities import Todo
from cq.app import EventSourcingApplication
from cq.contrib.sqlalchemy.storage import SqlAlchemyStorage


class TodoApp(EventSourcingApplication):
    storage_class = SqlAlchemyStorage
    storage_kwargs = {'db_uri': 'sqlite:///:memory:'}

    def __init__(self):
        super().__init__()
        self.repo = self.get_repo_for_entity(Todo)

    def add(self, name):
        uuid = self.genuuid()
        return self.repo.store('Todo.Added', uuid, data={'name': name})

    def finish(self, todo_id):
        self.repo.get_entity(todo_id)
        self.repo.store('Todo.Finished', todo_id)

    def reopen(self, todo_id):
        self.repo.get_entity(todo_id)
        self.repo.store('Todo.Reopened', todo_id)


todos = TodoApp()
