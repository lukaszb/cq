from . import app
from cq import handlers
from cq.events import Event
from cq.genuuid import genuuid
import pytest


@pytest.mark.parametrize('aggregate_type, name, expected_handlers', [
    ('User', 'Registered', {
        app.handle_user_registered,
        app.handle_all_user_events,
        app.handle_all_events,
    }),
    ('User', None, {
        app.handle_all_user_events,
        app.handle_all_events,
    }),
    ('Foo', 'Bar', {
        app.handle_all_events,
    }),
])
def test_get_handlers(aggregate_type, name, expected_handlers):
    event = Event(
        id=genuuid(),
        aggregate_type=aggregate_type,
        name=name,
        aggregate_id=genuuid(),
    )
    assert handlers.get_handlers(event) == expected_handlers
