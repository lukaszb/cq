from cq.contrib.django.models import Event as EventModel
from cq.contrib.django.models import UniqueItem
from cq.events import Event
from cq.storages import Storage
from django.db import IntegrityError


class DjangoStorage(Storage):

    def append(self, event):
        obj = to_model(event)
        obj.save()
        return from_model(obj)

    def iter_all_events(self):
        return (from_model(e) for e in EventModel.objects.order_by('ts').iterator())

    def get_events(self, aggregate_type, aggregate_id=None):
        qs = EventModel.objects.filter(aggregate_type=aggregate_type)
        if aggregate_id:
            qs = qs.filter(aggregate_id=aggregate_id)
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
        aggregate_type=event.aggregate_type,
        data=event.data,
        revision=event.revision,
    )


def from_model(instance):
    return Event(
        id=instance.id,
        name=instance.name,
        aggregate_id=instance.aggregate_id,
        aggregate_type=instance.aggregate_type,
        data=instance.data,
        ts=instance.ts,
        revision=instance.revision,
    )
