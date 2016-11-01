from django.conf.urls import include
from django.conf.urls import url
import accounts.urls


urlpatterns = [
    url(r'^api/auth/', include(accounts.urls)),
]
