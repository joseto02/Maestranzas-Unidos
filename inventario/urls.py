from django.urls import path
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("inventario/", views.inventario, name="inventario"),
    path("inventario/crear/", views.crear_producto, name="crear"),
    path("inventario/editar/<int:id>", views.editar_producto, name="editar"),
    path("inventario/eliminar/<int:id>", views.eliminar_producto, name="eliminar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
