from django.urls import path
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("inventario/", views.listar_productos, name="inventario"),
    path("inventario/crear/", views.crear_producto, name="crear"),
    path("inventario/editar/<int:id>", views.editar_producto, name="editar"),
    path("inventario/eliminar/<int:id>", views.eliminar_producto, name="eliminar"),
    path("entrada/", views.registrar_entrada, name="registrar_entrada"),
    path("salida/", views.registrar_salida, name="registrar_salida"),
    path("historial/<int:componente_id>/", views.historial_movimientos, name="historial_movimientos"),
    path('historial/', views.historial_general, name='historial_general'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
