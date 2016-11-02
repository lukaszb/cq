from ses.storages import LocalMemoryStorage
from ses.storages import Event
from ses.storages import Storage
from unittest import mock
import pytest


@pytest.fixture
def local_storage():
    return LocalMemoryStorage()


@mock.patch('ses.storages.publish')
def test_store(publish):
    storage = Storage()
    with mock.patch.object(storage, 'append', return_value='EVENT') as append:
        storage.store('User', 'Registered', 'aabbcc', data={'name': 'joe'})
        append.assert_called_once_with('User', 'Registered', 'aabbcc', {'name': 'joe'})
        publish.assert_called_once_with('EVENT')


def test_local__append(local_storage):
    local_storage.append('User', 'Registered', 'JOE_ID', data={'name': 'joe'})
    local_storage.append('User', 'Registered', 'JANE_ID', data={'name': 'jane'})
    local_storage.append('User', 'Activated', 'JOE_ID')

    assert local_storage.events == [
        Event('User', 'Registered', 'JOE_ID', {'name': 'joe'}),
        Event('User', 'Registered', 'JANE_ID', {'name': 'jane'}),
        Event('User', 'Activated', 'JOE_ID', None),
    ]


def test_local__get_events(local_storage):
    local_storage.append('User', 'Registered', 'JOE_ID', data={'name': 'joe'})
    local_storage.append('User', 'Registered', 'JANE_ID', data={'name': 'jane'})
    local_storage.append('User', 'Activated', 'JOE_ID')

    assert local_storage.get_events('JOE_ID') == [
        Event('User', 'Registered', 'JOE_ID', {'name': 'joe'}),
        Event('User', 'Activated', 'JOE_ID', None),
    ]
    assert local_storage.get_events('JANE_ID') == [
        Event('User', 'Registered', 'JANE_ID', {'name': 'jane'}),
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
