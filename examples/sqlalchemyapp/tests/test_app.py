from sqlalchemyapp.cqrs import TodoApp
import pytest


@pytest.fixture
def app():
    return TodoApp()


def test_add(app):
    todo_id = app.add('foo').entity_id
    todo = app.repo.get_entity(todo_id)
    assert todo.name == 'foo'
    assert todo.done is False


def test_finish(app):
    todo_id = app.add('foo').entity_id
    app.finish(todo_id)
    todo = app.repo.get_entity(todo_id)
    assert todo.name == 'foo'
    assert todo.done is True


def test_reopen(app):
    todo_id = app.add('foo').entity_id
    app.finish(todo_id)
    app.reopen(todo_id)
    todo = app.repo.get_entity(todo_id)
    assert todo.name == 'foo'
    assert todo.done is False


def test_get_events(app):
    todo_id_1 = app.add('foo').entity_id
    todo_id_2 = app.add('bar').entity_id

    app.finish(todo_id_1)
    app.reopen(todo_id_1)

    app.finish(todo_id_2)

    todo_1_events = [(e.entity_id, e.name) for e in app.repo.get_events(todo_id_1)]
    assert todo_1_events == [
        (todo_id_1, 'Todo.Added'),
        (todo_id_1, 'Todo.Finished'),
        (todo_id_1, 'Todo.Reopened'),
    ]

    todo_2_events = [(e.entity_id, e.name) for e in app.repo.get_events(todo_id_2)]
    assert todo_2_events == [
        (todo_id_2, 'Todo.Added'),
        (todo_id_2, 'Todo.Finished'),
    ]
