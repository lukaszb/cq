# from accounts import api
from accounts.cqrs import app
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory as BaseAPIRequestFactory
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
def test_no_auth(arf):
    request = arf.get('/api/auth/ping')

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def ping(request):
        assert request.user is None
        return Response({'msg': 'Pong!'})

    response = ping(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_auth_required(arf):
    user_id = app.register('joe@doe.com', 'secret').aggregate_id
    app.activate(user_id)
    event = app.obtain_auth_token(user_id)

    request = arf.get('/api/auth/ping', token=event.data['auth_token'])

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def ping(request):
        assert request.user is not None
        assert request.user.id == user_id
        assert request.user.is_active
        return Response({'msg': 'Pong!'})

    response = ping(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_auth_required_user_inactive(arf):
    user_id = app.register('joe@doe.com', 'secret').aggregate_id
    app.activate(user_id)
    event = app.obtain_auth_token(user_id)
    app.inactivate(user_id)

    request = arf.get('/api/auth/ping', token=event.data['auth_token'])

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def ping(request):
        assert request.user is None
        return Response({'msg': 'Pong!'})

    response = ping(request)
    assert response.status_code == 401
