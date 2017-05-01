import cq.aggregates
import cq.app


class User(cq.aggregates.Aggregate):

    def __init__(self, uuid):
        super().__init__(uuid)
        self.email = None


@cq.aggregates.register_mutator(User, 'Registered')
def mutate_registered(instance, event, data):
    instance.email = data['email']


@cq.aggregates.register_mutator(User, 'EmailChanged')
def mutate_email_changed(instance, event, data):
    instance.email = data['email']


def add_password(event):
    event.data['password'] = None


def add_role(event):
    event.data['role'] = 'user'


class Accounts(cq.app.BaseApp):

    def __init__(self):
        super().__init__()
        self.users = self.get_repo_for_aggregate(User)

    @cq.app.command
    def register(self, email, password=None, role='user'):
        uuid = self.genuuid()
        return self.users.store('Registered', uuid, data={
            'email': email,
            'password': password,
            'role': role,
        }, revision=3)

    @cq.app.command
    def change_email(self, user_id, email):
        return self.users.store('EmailChanged', user_id, data={'email': email})

    @cq.app.query
    def get(self, user_id):
        return self.users.get_aggregate(user_id)

    upcasters = [
        cq.app.upcaster('User', 'Registered', revision=1, method=add_password),
        cq.app.upcaster('User', 'Registered', revision=2, method=add_role),
    ]
