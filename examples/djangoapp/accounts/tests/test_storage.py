from accounts.cqrs import app
from cq.contrib.django.models import Event
import inspect
import pytest


@pytest.mark.django_db
def test_register(mocker):
    mocker.patch('accounts.cqrs.make_password', lambda p: 'encoded_s3cr3t')
    mocker.patch.object(app, 'genuuid', lambda: 'ACTIVATION_TOKEN')
    app.register(email='joe@doe.com', password='s3cr3t')

    assert Event.objects.count() == 1
    event = Event.objects.all().get()

    assert event.revision == 2


@pytest.mark.django_db
def test_iter_all_events():
    events = [
        app.register(email='joe@doe.com', password='s3cr3t'),
        app.register(email='kate@doe.com', password='s3cr3t'),
        app.register(email='mia@doe.com', password='s3cr3t'),
    ]

    assert inspect.isgenerator(app.storage.iter_all_events()) is True
    assert list(app.storage.iter_all_events()) == events
