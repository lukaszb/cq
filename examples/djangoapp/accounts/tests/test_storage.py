from accounts.cqrs import app
from cq.contrib.django.models import Event
import pytest


@pytest.mark.django_db
def test_register(mocker):
    mocker.patch('accounts.cqrs.make_password', lambda p: 'encoded_s3cr3t')
    mocker.patch.object(app, 'genuuid', lambda: 'ACTIVATION_TOKEN')
    app.register(email='joe@doe.com', password='s3cr3t')

    assert Event.objects.count() == 1
    event = Event.objects.all().get()

    assert event.revision == 1
