from cq.entities import Entity
from cq.entities import register_mutator


class User(Entity):
    __slots__ = ('email', 'encoded_password', 'activation_token', 'is_active')

    def is_authenticated(self):
        """
        Mimics what original Django's auth.User does
        """
        return self.is_active


@register_mutator(User, 'User.Registered')
def mutate_registered(entity, event, data):
    entity.email = data['email']
    entity.encoded_password = data['encoded_password']
    entity.activation_token = data['activation_token']
    entity.is_active = False


@register_mutator(User, 'User.ActivatedWithToken')
def mutate_activated_with_token(entity, event, data):
    entity.is_active = True
    entity.activation_token = None


@register_mutator(User, 'User.Activated')
def mutate_activated(entity, event, data):
    entity.is_active = True
    entity.activation_token = None


@register_mutator(User, 'User.Inactivated')
def mutate_inactivated(entity, event, data):
    entity.is_active = False
    entity.activation_token = None


@register_mutator(User, 'User.ObtainedAuthToken')
def mutate_obtained_auth_token(entity, event, data):
    entity.auth_token = data['auth_token']


def AnonymousUser():
    user = User(id=None)
    user.is_active = False
    user.email = None
    return user
