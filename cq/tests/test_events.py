from ..storages import LocalMemoryStorage
from ..storages import Storage
from cq import events
from datetime import datetime
from freezegun import freeze_time
from unittest import mock
import pytest


# Base `Event` class tests.

def test_assigns_all_properties():
    d = datetime.utcnow()
    e = events.Event(id='evt', aggregate_id='agg', ts=d, name='evt_name', data=None)

    assert e.id == 'evt'
    assert e.aggregate_id == 'agg'
    assert e.ts == d
    assert e.name == 'evt_name'


def test_requires_needed_properties():
    with pytest.raises(events.InvariantException) as exc:
        e = events.Event()


@freeze_time('2000-1-1')
@mock.patch.object(events, 'genuuid', return_value='evt_uuid')
def test_default_values_fields(_):
    e = events.Event(aggregate_id='agg', name='evt_name')

    assert e.id == 'evt_uuid'
    assert e.aggregate_id == 'agg'
    assert e.ts == datetime(2000, 1, 1)
    assert e.name == 'evt_name'


@freeze_time('2000-1-1')
@mock.patch.object(events, 'genuuid', return_value='evt_uuid')
def test_base_serialization(_):
    d = datetime.utcnow()
    e = events.Event(id='evt', aggregate_id='agg', ts=d, name='evt_name', data=None)

    assert e.serialize() == {
        'id': 'evt',
        'aggregate_id': 'agg',
        'data': None,
        'name': 'evt_name',
        'ts': '2000-01-01T00:00:00'
    }


# More complex tests against event data nesting & serialization

class UserCreatedEvent(events.EventBody):
    """
    Sample event body class for User.Created event.
    """
    name = events.field(mandatory=True, type=str)
    email = events.field(mandatory=True, type=str)
    age = events.field(type=int)


@freeze_time('2000-1-1')
def test_complex_serialization():
    data = UserCreatedEvent(name='John', email='john.doe@gmail.com', age=20)
    e = events.Event(id='evt', aggregate_id='agg', name='evt_name', data=data)

    assert e.serialize() == {
        'id': 'evt',
        'aggregate_id': 'agg',
        'name': 'evt_name',
        'ts': '2000-01-01T00:00:00',
        'data': {
            'name': 'John',
            'email': 'john.doe@gmail.com',
            'age': 20
        }
    }
