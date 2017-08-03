from cq.tests.app import Accounts
from cq import events
from cq.genuuid import genuuid


def test_event_is_upcasted():
    accounts = Accounts()

    event = accounts.register('joe@doe.com', password='secret')
    assert event.data == {'email': 'joe@doe.com', 'role': 'user', 'password': 'secret'}
    assert event.revision == 3


def test_event_upcast():

    event = events.Event(
        id=genuuid(),
        aggregate_type='User',
        name='Registered',
        aggregate_id=genuuid(),
        data={'email': 'joe@doe.com'},
    )

    assert event.revision == 1

    upcasters = [
        events.upcaster('User', 'Registered', revision=1, method=add_role),
        events.upcaster('User', 'Registered', revision=2, method=add_fullname),
        events.upcaster('User', 'ChangedRole', revision=1, method=noop),
    ]

    events.upcast(event, upcasters)

    assert event.revision == 3
    assert event.data == {
        'email': 'joe@doe.com',
        'role': 'user',
        'fullname': None,
    }


def test_event_upcast__only_needed_upcasters_are_used():

    event = events.Event(
        id=genuuid(),
        aggregate_type='User',
        name='Registered',
        aggregate_id=genuuid(),
        data={'email': 'joe@doe.com', 'role': 'admin'},
        revision=2,
    )

    upcasters = [
        events.upcaster('User', 'Registered', revision=1, method=add_role),
        events.upcaster('User', 'Registered', revision=2, method=add_fullname),
        events.upcaster('User', 'ChangedRole', revision=1, method=noop),
    ]

    events.upcast(event, upcasters)

    assert event.revision == 3
    assert event.data == {
        'email': 'joe@doe.com',
        'role': 'admin',
        'fullname': None,
    }


def add_role(event):
    event.data['role'] = 'user'


def add_fullname(event):
    event.data['fullname'] = None


def noop(event):
    pass
