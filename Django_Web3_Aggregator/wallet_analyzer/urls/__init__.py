from django.urls import include, path
from .urls import urlpatterns, app_name

urlpatterns = [
    path('wallets/', include(urlpatterns)),
]