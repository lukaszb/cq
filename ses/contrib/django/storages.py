from django.db import IntegrityError
from ses.contrib.django.models import Event
from ses.contrib.django.models import UniqueItem
from ses.storages import Storage


class DjangoStorage(Storage):

    def append(self, entity, action, entity_id, data=None):
        return Event.objects.create(
            entity_id=entity_id,
            entity=entity,
            action=action,
            data=data,
        )

    def get_events(self, entity_id):
        return Event.objects.filter(entity_id=entity_id).order_by('id')

    def book_unique(self, namespace, value, entity_id):
        try:
            UniqueItem.objects.create(namespace=namespace, value=value, entity_id=entity_id)
        except IntegrityError:
            msg = 'Value %r already exists within %r namespace' % (value, namespace)
            raise Storage.DuplicatedItemError(msg)

    def get_unique(self, namespace, value):
        try:
            return UniqueItem.objects.get(namespace=namespace, value=value).entity_id
        except UniqueItem.DoesNotExist:
            return None
