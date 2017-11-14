import cq.aggregates
import cq.app
import cq.handlers
import cq.schemas


def add_password(event):
    event.data['password'] = None


def add_role(event):
    event.data['role'] = 'user'


class User(cq.aggregates.Aggregate):

    def __init__(self, uuid):
        super().__init__(uuid)
        self.email = None

    upcasters = [
        cq.aggregates.upcaster('User', 'Registered', revision=1, method=add_password),
        cq.aggregates.upcaster('User', 'Registered', revision=2, method=add_role),
    ]

class UserRegisteredSchema(cq.schemas.EventSchema):
    email = cq.schemas.fields.Email()
    password = cq.schemas.fields.Str()
    role = cq.schemas.fields.Str()


class UserEmailChangedSchema(cq.schemas.EventSchema):
    email = cq.schemas.fields.Email()


@cq.aggregates.register_mutator(User, 'Registered', schema=UserRegisteredSchema)
def mutate_registered(instance, event, data):
    instance.email = data['email']
    instance.password = data['password']
    instance.role = data['role']


@cq.aggregates.register_mutator(User, 'EmailChanged', schema=UserEmailChangedSchema)
def mutate_email_changed(instance, event, data):
    instance.email = data['email']


class Accounts(cq.app.BaseApp):
    repos = {'users': User}

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


@cq.handlers.register_handler('User', 'Registered')
def handle_user_registered(event, replaying_events):
    update_projection()
    if not replaying_events:
        send_email()


@cq.handlers.register_handler('User', 'EmailChanged')
def handle_user_email_changed(event, replaying_events):
    pass


def update_projection():
    """
    Dummy function (mocked at tests)
    """


def send_email():
    """
    Dummy function (mocked at tests)
    """


@cq.handlers.register_handler('User')
def handle_all_user_events(event, replaying_events):
    pass


@cq.handlers.register_handler()
def handle_all_events(event, replaying_events):
    pass
