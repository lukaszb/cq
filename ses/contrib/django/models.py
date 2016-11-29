from django.db import models
from django.utils import timezone
from ses.genuuid import genuuid
import jsonfield


class Event(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=genuuid)
    ts = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=128, db_index=True)
    entity_id = models.CharField(max_length=128, db_index=True)
    data = jsonfield.JSONField(null=True)

    def __str__(self):
        return '%s | %s | %s' % (self.name, self.entity_id, self.ts)


class UniqueItem(models.Model):
    namespace = models.CharField(max_length=128)
    value = models.CharField(max_length=255)
    entity_id = models.CharField(max_length=128)

    class Meta:
        unique_together = ('namespace', 'value')

    def __str__(self):
        return '%s | %s' % (self.namespace, self.value)
