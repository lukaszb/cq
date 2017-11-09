from . import app
from unittest import mock
import cq.handlers


@mock.patch.object(app, 'update_projection')
@mock.patch.object(app, 'send_email')
def test_replay_events(send_email, update_projection):
    accounts = app.Accounts()

    with mock.patch.object(app, 'update_projection') as update_projection, \
            mock.patch.object(app, 'send_email') as send_email:
        user_id = accounts.genuuid()
        accounts.users.store('Registered', user_id, data={'email': 'joe@doe.com'}, revision=1)
        accounts.users.store('Registered', user_id, data={'email': 'kate@doe.com', 'password': 'secret'}, revision=2)

        assert update_projection.call_args_list == [mock.call(), mock.call()]
        assert send_email.call_args_list == [mock.call(), mock.call()]

    with mock.patch.object(app, 'update_projection') as update_projection, \
            mock.patch.object(app, 'send_email') as send_email:

        accounts.storage.replay_events()

        assert update_projection.call_args_list == [mock.call(), mock.call()]
        assert not send_email.called


def test_replay_events_generator():
    accounts = app.Accounts()
    user_id = accounts.genuuid()
    event1 = accounts.users.store('Registered', user_id, data={'email': 'joe@doe.com'}, revision=1)
    event2 = accounts.users.store('Registered', user_id, data={'email': 'kate@doe.com', 'password': 'secret'}, revision=2)

    replayed_events_ids = []
    with mock.patch.object(app, 'update_projection') as update_projection:
        for event in accounts.storage.gen_replay_events():
            replayed_events_ids.append(event.id)

        assert update_projection.call_args_list == [mock.call(), mock.call()]

    assert replayed_events_ids == [event1.id, event2.id]


def test_replay_events__passes_upcasted_events_to_handlers():
    accounts = app.Accounts()
    user_id = accounts.genuuid()

    event = accounts.storage.store('User', 'Registered', user_id, data={'email': 'joe@doe.com'}, revision=1)
    assert event.data == {'email': 'joe@doe.com'}  # data was not upcasted yet

    handler = mock.Mock()

    with mock.patch.object(cq.handlers, 'get_handlers', lambda e: {handler}):
        accounts.storage.replay_events(upcasters=app.User.upcasters)
        assert handler.called is True
        call_args, call_kwargs = handler.call_args
        event_passed_to_handler = call_kwargs['event']
        # make sure event passed to handler were upcasted
        assert event_passed_to_handler.data == {
            'email': 'joe@doe.com',
            'password': None,
            'role': 'user',
        }
