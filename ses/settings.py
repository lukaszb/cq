from django.utils.module_loading import import_string


DEFAULT_STORAGE_CLASS = import_string('ses.contrib.django.storages.DjangoStorage')
