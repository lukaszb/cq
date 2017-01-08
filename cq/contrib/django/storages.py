from cq.contrib.django.models import Event as EventModel
from cq.contrib.django.models import UniqueItem
from cq.events import Event
from cq.storages import Storage
from django.db import IntegrityError


class DjangoStorage(Storage):

    def append(self, event):
        obj = to_model(event)
        obj.save()
        return obj

    def get_events(self, entity_id):
        qs = EventModel.objects.filter(entity_id=entity_id).order_by('ts')
        return (from_model(e) for e in qs)

    def book_unique(self, namespace, value, entity_id):
        try:
            UniqueItem.objects.create(namespace=namespace, value=value, entity_id=entity_id)
        except IntegrityError:
            raise Storage.DuplicatedItemError('%s:%s already exists' % (namespace, value))

    def get_unique(self, namespace, value):
        try:
            return UniqueItem.objects.get(namespace=namespace, value=value).entity_id
        except UniqueItem.DoesNotExist:
            raise self.DoesNotExist('%s:%s was not set' % (namespace, value))

    def has_unique(self, namespace, value):
        return UniqueItem.objects.filter(namespace=namespace, value=value).exists()


def to_model(event):
    return EventModel(
        id=event.id,
        name=event.name,
        entity_id=event.entity_id,
        data=event.data,
    )


def from_model(instance):
    return Event(
        id=instance.id,
        name=instance.name,
        entity_id=instance.entity_id,
        data=instance.data,
        ts=instance.ts,
    )
