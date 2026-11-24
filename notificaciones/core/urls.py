from django.contrib import admin
from django.urls import path
from gestion_notificaciones.views import notificar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notificar', notificar, name='notificar'),
]