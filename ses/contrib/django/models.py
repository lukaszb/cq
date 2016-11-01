from django.db import models
from django.utils import timezone
import jsonfield


class Event(models.Model):
    ts = models.DateTimeField(default=timezone.now)
    entity_id = models.CharField(max_length=128, db_index=True)
    entity = models.CharField(max_length=255, db_index=True)
    action = models.CharField(max_length=255, db_index=True)
    data = jsonfield.JSONField(null=True)

    def __str__(self):
        return '%s | %s | %s' % (self.action, self.entity_id, self.ts)

    def get_entity_action(self):
        return '%s.%s' % (self.entity, self.action)


class UniqueItem(models.Model):
    namespace = models.CharField(max_length=128)
    value = models.CharField(max_length=255)
    entity_id = models.CharField(max_length=128)

    class Meta:
        unique_together = ('namespace', 'value')

    def __str__(self):
        return '%s | %s' % (self.namespace, self.value)
