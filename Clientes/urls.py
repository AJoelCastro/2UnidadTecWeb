from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente_list, name='cliente_list'),
    path('crear/', views.cliente_create, name='cliente_create'),
    path('editar/<int:pk>/', views.cliente_update, name='cliente_update'),
    path('eliminar/<int:pk>/', views.cliente_delete, name='cliente_delete'),
]