from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.lista_categorias, name='lista_categorias'),
    path('editar/', views.editar_categoria, name='Editar Categorias'),
    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('eliminar/', views.eliminar_categoria, name='Eliminar Categorias'),
]