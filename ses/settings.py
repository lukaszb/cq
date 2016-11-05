from django.utils.module_loading import import_string
import os


DEFAULT_STORAGE_CLASS = import_string('ses.storages.LocalMemoryStorage')
DB_URI = os.environ.get('DB_URI')
ENGINE_ECHO = 'SES_SQLALCHEMY_ENGINE_ECHO' in os.environ


# if Django is configured default storage would be Django specific one
# unless user explicitly set SES_DEFAULT_STORAGE_CLASS at settings
# pointing to another storage
try:
    from django.conf import settings
    if settings.configured:
        cls = getattr(settings, 'SES_DEFAULT_STORAGE_CLASS',
                      'ses.contrib.django.storages.DjangoStorage')
        DEFAULT_STORAGE_CLASS = import_string(cls)
except ImportError:
    # we are not in a Django context, do nothing
    pass
