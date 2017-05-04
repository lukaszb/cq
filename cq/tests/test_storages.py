from ..storages import Storage
from unittest import mock
import inspect
import pytest


@mock.patch('cq.storages.genuuid', lambda: 'EVENT_ID')
@mock.patch('cq.storages.handle_event')
def test_store(handle_event):
    storage = Storage()
    with mock.patch.object(storage, 'create_event', return_value='EVENT') as create_event,\
            mock.patch.object(storage, 'append', return_value='APPENDED_EVENT') as append:
        storage.store('User', 'Registered', 'aabbcc', {'name': 'joe'})
        create_event.assert_called_once_with(
            id='EVENT_ID',
            aggregate_type='User',
            name='Registered',
            aggregate_id='aabbcc',
            data={'name': 'joe'},
            ts=None,
            revision=1,
        )
        append.assert_called_once_with('EVENT')
        handle_event.assert_called_once_with('APPENDED_EVENT', replaying_events=False)


def test_local__append(local_storage):
    local_storage.store('User', 'Registered', 'JOE_ID', {'name': 'joe'}, 'TS')
    local_storage.store('User', 'Registered', 'JANE_ID', {'name': 'jane'}, 'TS')
    local_storage.store('User', 'Activated', 'JOE_ID', ts='TS')

    assert [(e.name, e.aggregate_id, e.data, e.ts) for e in local_storage.events] == [
        ('Registered', 'JOE_ID', {'name': 'joe'}, 'TS'),
        ('Registered', 'JANE_ID', {'name': 'jane'}, 'TS'),
        ('Activated', 'JOE_ID', None, 'TS'),
    ]


def test_local__get_events(local_storage):
    local_storage.store('User', 'Registered', 'JOE_ID', {'name': 'joe'}, 'TS')
    local_storage.store('User', 'Registered', 'JANE_ID', {'name': 'jane'}, 'TS')
    local_storage.store('User', 'Activated', 'JOE_ID', {'name': 'joe'}, 'TS')

    assert [(e.name, e.aggregate_id) for e in local_storage.get_events('User', 'JOE_ID')] == [
        ('Registered', 'JOE_ID'),
        ('Activated', 'JOE_ID'),
    ]
    assert [(e.name, e.aggregate_id) for e in local_storage.get_events('User', 'JANE_ID')] == [
        ('Registered', 'JANE_ID'),
    ]


def test_local__get_events_with_same_aggregate_id_among_various_event_types(local_storage):
    local_storage.store('User', 'Registered', 'JOE_ID', {'name': 'joe'}, 'TS')
    local_storage.store('User', 'Activated', 'JOE_ID', {'name': 'joe'}, 'TS')
    local_storage.store('User', 'Registered', 'JANE_ID', {'name': 'jane'}, 'TS')
    local_storage.store('Project', 'Follows', 'JOE_ID', {'project_id': 'PROJECT1_ID'}, 'TS')
    local_storage.store('Project', 'Follows', 'JOE_ID', {'project_id': 'PROJECT2_ID'}, 'TS')

    assert [(e.name, e.aggregate_id) for e in local_storage.get_events('User', 'JOE_ID')] == [
        ('Registered', 'JOE_ID'),
        ('Activated', 'JOE_ID'),
    ]
    assert [(e.name, e.aggregate_id) for e in local_storage.get_events('Project', 'JOE_ID')] == [
        ('Follows', 'JOE_ID'),
        ('Follows', 'JOE_ID'),
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


def test_local__iter_all_events(local_storage):
    all_events = [
        local_storage.store('User', 'Registered', 'JOE_ID', {'name': 'joe'}, 'TS'),
        local_storage.store('User', 'Activated', 'JOE_ID', {'name': 'joe'}, 'TS'),
        local_storage.store('User', 'Registered', 'JANE_ID', {'name': 'jane'}, 'TS'),
    ]

    assert inspect.isgenerator(local_storage.iter_all_events()) is True
    assert list(local_storage.iter_all_events()) == all_events
