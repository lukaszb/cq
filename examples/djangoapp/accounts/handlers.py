from .models import User as UserProjection
from ses.handlers import register_handler


@register_handler('User.Registered')
def handle_registered_user(event):
    UserProjection.objects.create(
        id=event.entity_id,
        email=event.data['email'],
        registered_at=event.ts,
    )
    # send email with activation token etc
