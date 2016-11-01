from ses.entities import Entity
from ses.entities import register_mutator


class User(Entity):
    Registered = Entity.Action()
    ActivatedWithToken = Entity.Action()
    Activated = Entity.Action()
    Inactivated = Entity.Action()
    ObtainedAuthToken = Entity.Action()

    __slots__ = ('email', 'encoded_password', 'activation_token', 'is_active')

    def is_authenticated(self):
        """
        Mimics what original Django's auth.User does
        """
        return self.is_active


@register_mutator(User.Registered)
def mutate_registered(self, data):
    self.email = data['email']
    self.encoded_password = data['encoded_password']
    self.activation_token = data['activation_token']
    self.is_active = False


@register_mutator(User.ActivatedWithToken)
def mutate_activated_with_token(self, data):
    self.is_active = True
    self.activation_token = None


@register_mutator(User.Activated)
def mutate_activated(self, data):
    self.is_active = True
    self.activation_token = None


@register_mutator(User.Inactivated)
def mutate_inactivated(self, data):
    self.is_active = False
    self.activation_token = None


@register_mutator(User.ObtainedAuthToken)
def mutate_obtained_auth_token(self, data):
    self.auth_token = data['auth_token']


def AnonymousUser():
    user = User(id=None)
    user.is_active = False
    user.email = None
    return user
