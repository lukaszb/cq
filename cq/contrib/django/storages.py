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

    def get_events(self, aggregate_type, aggregate_id):
        type_prefix = aggregate_type + '.'
        qs = EventModel.objects.filter(aggregate_id=aggregate_id, name__startswith=type_prefix)
        qs = qs.order_by('ts')
        return (from_model(e) for e in qs)

    def book_unique(self, namespace, value, aggregate_id):
        try:
            UniqueItem.objects.create(namespace=namespace, value=value, aggregate_id=aggregate_id)
        except IntegrityError:
            raise Storage.DuplicatedItemError('%s:%s already exists' % (namespace, value))

    def get_unique(self, namespace, value):
        try:
            return UniqueItem.objects.get(namespace=namespace, value=value).aggregate_id
        except UniqueItem.DoesNotExist:
            raise self.DoesNotExist('%s:%s was not set' % (namespace, value))

    def has_unique(self, namespace, value):
        return UniqueItem.objects.filter(namespace=namespace, value=value).exists()


def to_model(event):
    return EventModel(
        id=event.id,
        name=event.name,
        aggregate_id=event.aggregate_id,
        data=event.data,
    )


def from_model(instance):
    return Event(
        id=instance.id,
        name=instance.name,
        aggregate_id=instance.aggregate_id,
        data=instance.data,
        ts=instance.ts,
    )
