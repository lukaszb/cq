from .app import Accounts
import cq.aggregates


class User(cq.aggregates.Aggregate):
    pass


class Project(cq.aggregates.Aggregate):
    pass


def test_register_mutators_set_mutator_for_subclass():

    @cq.aggregates.register_mutator(User, 'Created')
    def user_created(instance, event, data):
        pass

    @cq.aggregates.register_mutator(Project, 'Created')
    def project_created(instance, event, data):
        pass

    assert User.mutators == {'Created': user_created}
    assert Project.mutators == {'Created': project_created}


def test_aggregate_is_rehydrated_with_upcasted_events():
    accounts = Accounts()
    user_id = accounts.genuuid()
    accounts.storage.store('User', 'Registered', user_id, data={'email': 'joe@doe.com'})
    user = accounts.users.get_aggregate(user_id)
    assert user.role == 'user'
