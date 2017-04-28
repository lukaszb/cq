from __future__ import unicode_literals
from django.db import migrations, models


def split_event_names(apps, schema_editor):
    Event = apps.get_model('cq', 'Event')
    for event in Event.objects.all():
        event.aggregate_type, event.name = event.name.split('.', 1)
        event.save(update_fields=['aggregate_type', 'name'])


def join_event_names(apps, schema_editor):
    Event = apps.get_model('cq', 'Event')
    for event in Event.objects.all():
        event.aggregate_type, event.name = event.name.split('.', 1)
        event.name = '%s.%s' % (event.aggregate_type, event.name)


class Migration(migrations.Migration):

    dependencies = [
        ('cq', '0002_ts_field_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='aggregate_type',
            field=models.CharField(db_index=True, max_length=128, null=True),
        ),
        migrations.RunPython(split_event_names, join_event_names),
        # now we can make aggregate_type non-nullable
        migrations.AlterField(
            model_name='event',
            name='aggregate_type',
            field=models.CharField(db_index=True, max_length=128),
        ),
    ]
