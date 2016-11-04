import datetime


class Event:
    def __init__(self, name, entity_id, data=None, ts=None):
        self.name = name
        self.entity_id = entity_id
        self.data = data
        self.ts = ts or datetime.datetime.now()

    def __str__(self):
        return '%s | %s | %s' % (self.name, self.entity_id, self.ts)
