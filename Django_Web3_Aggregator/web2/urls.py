from django.urls import path
from . import views  # Импортируйте ваши представления

urlpatterns = [
    # Добавьте ваши маршруты
    path('', views.Web2.as_view(), name='base.html'),  # Например, маршрут для главной страницы
]
