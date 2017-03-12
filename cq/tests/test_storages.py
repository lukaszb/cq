from ..genuuid import genuuid
from ..storages import LocalMemoryStorage
from ..storages import Storage
from datetime import datetime
from pyrsistent import PRecord, field
from unittest import mock
import pytest


@pytest.fixture
def local_storage():
    return LocalMemoryStorage()


@mock.patch('cq.storages.genuuid', lambda: 'EVENT_ID')
@mock.patch('cq.storages.publish')
def test_store(publish):
    storage = Storage()
    with mock.patch.object(storage, 'create_event', return_value='EVENT') as create_event,\
         mock.patch.object(storage, 'append') as append:
        storage.store('User.Registered', 'aabbcc', {'name': 'joe'})
        create_event.assert_called_once_with(
            id='EVENT_ID',
            name='User.Registered',
            aggregate_id='aabbcc',
            data={'name': 'joe'},
            ts=None,
        )
        append.assert_called_once_with('EVENT')
        publish.assert_called_once_with('EVENT')


def test_local__append(local_storage):
    ts = datetime.utcnow()

    local_storage.store('User.Registered', 'JOE_ID', {'name': 'joe'}, ts)
    local_storage.store('User.Registered', 'JANE_ID', {'name': 'jane'}, ts)
    local_storage.store('User.Activated', 'JOE_ID', ts=ts)

    assert [(e.name, e.aggregate_id, e.data, e.ts) for e in local_storage.events] == [
        ('User.Registered', 'JOE_ID', {'name': 'joe'}, ts),
        ('User.Registered', 'JANE_ID', {'name': 'jane'}, ts),
        ('User.Activated', 'JOE_ID', None, ts),
    ]


def test_local__get_events(local_storage):
    ts = datetime.utcnow()

    local_storage.store('User.Registered', 'JOE_ID', {'name': 'joe'}, ts)
    local_storage.store('User.Registered', 'JANE_ID', {'name': 'jane'}, ts)
    local_storage.store('User.Activated', 'JOE_ID', {'name': 'joe'}, ts)

    assert [(e.name, e.aggregate_id) for e in local_storage.get_events('JOE_ID')] == [
        ('User.Registered', 'JOE_ID'),
        ('User.Activated', 'JOE_ID'),
    ]
    assert [(e.name, e.aggregate_id) for e in local_storage.get_events('JANE_ID')] == [
        ('User.Registered', 'JANE_ID'),
    ]


def test_local__book_unique(local_storage):
    local_storage.book_unique('user_email', 'joe@doe.com', 'JOE_ID')
    assert local_storage.has_unique('user_email', 'joe@doe.com') is True
    assert local_storage.get_unique('user_email', 'joe@doe.com') == 'JOE_ID'


def test_local__book_unique_fails_for_duplicate(local_storage):
    local_storage.book_unique('user_email', 'joe@doe.com', 'JOE_ID')

    with pytest.raises(Storage.DuplicatedItemError):
        local_storage.book_unique('user_email', 'joe@doe.com', 'JOE_ID2')

    # first value should not be overridden
    assert local_storage.get_unique('user_email', 'joe@doe.com') == 'JOE_ID'
