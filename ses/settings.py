from django.utils.module_loading import import_string
import os


DEFAULT_STORAGE_CLASS = import_string('ses.storages.LocalMemoryStorage')
DB_URI = os.environ.get('DB_URI')
ENGINE_ECHO = 'SES_SQLALCHEMY_ENGINE_ECHO' in os.environ
