from .app import Accounts


def test_aggregate_version_is_bumped():
    accounts = Accounts()
    user_id = accounts.register('joe@doe.com', password='secret').aggregate_id
    user = accounts.get(user_id)

    assert user.email == 'joe@doe.com'
    assert user.version == 1

    accounts.change_email(user_id, 'jerry@doe.com')
    user = accounts.get(user_id)

    assert user.email == 'jerry@doe.com'
    assert user.version == 2
