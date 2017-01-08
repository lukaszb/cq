from django.db import models
from django.utils import timezone
from cq.genuuid import genuuid
import jsonfield


class Event(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=genuuid)
    ts = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=128, db_index=True)
    aggregate_id = models.CharField(max_length=128, db_index=True)
    data = jsonfield.JSONField(null=True)

    def __str__(self):
        return '%s | %s | %s' % (self.action, self.aggregate_id, self.ts)

    def get_aggregate_action(self):
        return '%s.%s' % (self.aggregate, self.action)


class UniqueItem(models.Model):
    namespace = models.CharField(max_length=128)
    value = models.CharField(max_length=255)
    aggregate_id = models.CharField(max_length=128)

    class Meta:
        unique_together = ('namespace', 'value')

    def __str__(self):
        return '%s | %s' % (self.namespace, self.value)
