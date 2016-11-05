from accounts.cqrs import app
import pytest


@pytest.mark.django_db
def test_register(mocker):
    mocker.patch('accounts.cqrs.make_password', lambda p: 'encoded_s3cr3t')
    mocker.patch.object(app, 'genuuid', lambda: 'ACTIVATION_TOKEN')
    event = app.register(email='joe@doe.com', password='s3cr3t')
    assert event.data == {
        'email': 'joe@doe.com',
        'encoded_password': 'encoded_s3cr3t',
        'activation_token': 'ACTIVATION_TOKEN',
    }


@pytest.mark.django_db
def test_activate_with_token(mocker):
    event = app.register(email='joe@doe.com', password='s3cr3t')
    user = app.repo.get_entity(event.entity_id)
    event = app.activate_with_token(user.id, user.activation_token)
    user.mutate(event)
    assert user.is_active


@pytest.mark.django_db
def test_activate_with_token__fails_for_already_active_members(mocker):
    event = app.register(email='joe@doe.com', password='s3cr3t')
    app.activate(event.entity_id)
    user = app.repo.get_entity(event.entity_id)
    with pytest.raises(AssertionError):
        app.activate_with_token(user.id, user.activation_token)


@pytest.mark.django_db
def test_obtain_auth_token(mocker):
    event = app.register(email='joe@doe.com', password='s3cr3t')
    app.activate(event.entity_id)

    mocker.patch.object(app, 'genuuid', lambda: 'AUTH_TOKEN')
    event = app.obtain_auth_token(event.entity_id)
    assert event.data['auth_token'] == 'AUTH_TOKEN'


@pytest.mark.django_db
def test_obtain_auth_token__inactive_user():
    event = app.register(email='joe@doe.com', password='s3cr3t')

    with pytest.raises(AssertionError):
        app.obtain_auth_token(event.entity_id)
