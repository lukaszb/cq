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
