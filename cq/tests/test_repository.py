from . import app
import cq.aggregates
import cq.genuuid


class UserRepo(cq.aggregates.Repository):
    aggregate_class = app.User


def test_upcast_event(local_storage):
    repo = UserRepo(local_storage)
    user_id = cq.genuuid.genuuid()

    event = repo.store('Registered', user_id, data={'email': 'joe@doe.com'}, revision=1)
    assert event.data == {
        'email': 'joe@doe.com',
        'password': None,
        'role': 'user',
    }

    event = repo.store('Registered', user_id, data={
        'email': 'joe@doe.com',
        'password': 'secret',
        'role': 'admin',  # this would be overridden as it should not be there (yet - at revision=2)
    }, revision=2)
    assert event.data == {
        'email': 'joe@doe.com',
        'password': 'secret',
        'role': 'user',
    }

    event = repo.store('Registered', user_id, data={
        'email': 'joe@doe.com',
        'password': 'secret',
        'role': 'admin',
    }, revision=3)
    assert event.data == {
        'email': 'joe@doe.com',
        'password': 'secret',
        'role': 'admin',
    }
