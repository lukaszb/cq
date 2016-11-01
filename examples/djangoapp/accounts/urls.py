from django.conf.urls import url
from . import api


urlpatterns = [
    url(r'^register$', api.register),
    url(r'^activate/(?P<user_id>[-\w]+)$', api.activate),
    url(r'^me$', api.profile),
    url(r'^obtain-auth-token$', api.obtain_auth_token),
]
