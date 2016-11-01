# from accounts import api
from accounts import api
from accounts.models import User as UserProjection
from freezegun import freeze_time
from rest_framework.test import APIRequestFactory as BaseAPIRequestFactory
import datetime
import pytest


class APIRequestFactory(BaseAPIRequestFactory):
    def request(self, **kwargs):
        token = kwargs.pop('token', None)
        if token is not None:
            kwargs['HTTP_AUTHORIZATION'] = 'Token %s' % token
        request = super().request(**kwargs)
        return request


@pytest.fixture
def arf():
    return APIRequestFactory()


@pytest.mark.django_db
def test_register(arf):
    request = arf.post('/api/auth/register', data={
        'email': 'joe@doe.com',
        'password': 'secret',
    })
    with freeze_time('2016-10-21 14:30'):
        response = api.register(request)
    assert response.status_code == 200

    qs = UserProjection.objects.filter(email='joe@doe.com')
    assert qs.exists() is True
    user = qs.get()
    assert user.registered_at == datetime.datetime(2016, 10, 21, 14, 30)
