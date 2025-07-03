from django.urls import path
from . import views
from .utils import generate_pdf

urlpatterns = [
    path('', views.listar_venta, name='listar_venta'),
    path('crear/', views.agregar_venta, name='crear_venta'),
    path('editar/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('anular/<int:pk>/', views.anular_venta, name='eliminar_venta'),
    path('api/producto-info/', views.get_producto_info, name='get_producto_info'),
    path('api/serie-info/', views.get_serie_info, name='get_serie_info'),
    path('pdf/<int:venta_id>/', generate_pdf, name='generar_pdf'),
]