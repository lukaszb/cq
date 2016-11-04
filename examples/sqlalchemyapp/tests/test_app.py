from sqlalchemyapp.cqrs import TodoApp
import pytest


@pytest.fixture
def app():
    return TodoApp()


def test_add(app):
    todo_id = app.add('foo').entity_id
    todo = app.repo.get_entity(todo_id)
    assert todo.name == 'foo'
