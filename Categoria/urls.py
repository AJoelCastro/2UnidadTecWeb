from django.urls import path
from . import views

urlpatterns = [
    path('', views.categoria_list, name='categoria_list'),
    path('crear/', views.categoria_create, name='categoria_create'),
    path('editar/<int:pk>/', views.categoria_update, name='categoria_update'),
    path('eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),
]