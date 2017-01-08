from django.apps import AppConfig
from django.apps import apps
from django.utils.module_loading import import_module
import os.path


class SimpleEventSourcingApp(AppConfig):
    name = 'cq.contrib.django'
    label = 'cq'
    verbose_name = 'Simple Event Store App'

    def ready(self):
        for name, app in apps.app_configs.items():
            import_handlers_module(app.name)


def import_handlers_module(app_module_name):
    handlers_module_name = '%s.handlers' % app_module_name
    try:
        import_module(handlers_module_name)
    except ImportError:
        # we need to re-raise exception in case there was import errors inside
        # handlers.py module
        handlers_file_name = get_handlers_file_name(app_module_name)
        if os.path.exists(handlers_file_name):
            raise


def get_handlers_file_name(app_module_name):
    module = import_module(app_module_name)
    module_dir = os.path.dirname(module.__file__)
    return os.path.join(module_dir, 'handlers.py')
