from cq.aggregates import Aggregate
from cq.aggregates import register_mutator
from cq.schemas import EventSchema
from cq.schemas import fields


class User(Aggregate):
    __slots__ = ('email', 'encoded_password', 'activation_token', 'is_active')

    def is_authenticated(self):
        """
        Mimics what original Django's auth.User does
        """
        return self.is_active


class UserRegisteredSchema(EventSchema):
    email = fields.Email()
    encoded_password = fields.Str()
    activation_token = fields.Str()
    role = fields.Str()


class ActivatedWithTokenSchema(EventSchema):
    pass


class ActivatedSchema(EventSchema):
    pass


class InactivatedSchema(EventSchema):
    pass


class ObtainedAuthTokenSchema(EventSchema):
    auth_token = fields.Str()


@register_mutator(User, 'Registered', schema=UserRegisteredSchema)
def mutate_registered(aggregate, event, data):
    aggregate.email = data['email']
    aggregate.encoded_password = data['encoded_password']
    aggregate.activation_token = data['activation_token']
    aggregate.is_active = False


@register_mutator(User, 'ActivatedWithToken', schema=ActivatedWithTokenSchema)
def mutate_activated_with_token(aggregate, event, data):
    aggregate.is_active = True
    aggregate.activation_token = None


@register_mutator(User, 'Activated', schema=ActivatedSchema)
def mutate_activated(aggregate, event, data):
    aggregate.is_active = True
    aggregate.activation_token = None


@register_mutator(User, 'Inactivated', schema=InactivatedSchema)
def mutate_inactivated(aggregate, event, data):
    aggregate.is_active = False
    aggregate.activation_token = None


@register_mutator(User, 'ObtainedAuthToken', schema=ObtainedAuthTokenSchema)
def mutate_obtained_auth_token(aggregate, event, data):
    aggregate.auth_token = data['auth_token']


def AnonymousUser():
    user = User(id=None)
    user.is_active = False
    user.email = None
    return user
