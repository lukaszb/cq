import random
import string
import django

DEBUG = False

SECRET_KEY = ''.join([random.choice(string.ascii_letters) for x in range(40)])


INSTALLED_APPS = (
    'cq.contrib.django.apps.SimpleEventSourcingApp',
    # 'cq',
    'accounts',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
)

if django.VERSION < (1, 10):
    MIDDLEWARE_CLASSES = MIDDLEWARE

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ROOT_URLCONF = 'urls'
SITE_ID = 1


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

TEMPLATES = []

# =============================================================================
# djangorestframework
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'accounts.auth.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'UNAUTHENTICATED_USER': 'accounts.entities.AnonymousUser',
}
