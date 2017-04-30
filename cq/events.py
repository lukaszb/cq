from collections import namedtuple
import datetime


upcaster = namedtuple('Upcaster', 'aggregate_type, event_name, revision, method')


class Event:
    def __init__(self, id, aggregate_type, name, aggregate_id, data=None, ts=None, revision=1):
        self.id = id
        self.aggregate_type = aggregate_type
        self.name = name
        self.aggregate_id = aggregate_id
        self.data = data
        self.ts = ts or datetime.datetime.now()
        self.revision = revision

    def __str__(self):
        return '%s.%s | %s | %s' % (self.aggregate_type, self.name, self.aggregate_id, self.ts)


def upcast(event, upcasters):
    event_upcasters = get_upcasters_for_event(event, upcasters)
    for upcaster in event_upcasters:
        single_upcast(event, upcaster)


def single_upcast(event, upcaster):
    upcaster.method(event)
    event.revision += 1


def get_upcasters_for_event(event, upcasters):

    def matches_event(upcaster):
        return (upcaster.aggregate_type == event.aggregate_type and
                upcaster.event_name == event.name and
                upcaster.revision >= event.revision)

    relevant_upcasters = [upcaster for upcaster in upcasters if matches_event(upcaster)]
    relevant_upcasters.sort(key=lambda upcaster: upcaster.revision)
    return relevant_upcasters
