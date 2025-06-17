
from django.contrib import admin
from django.urls import path,include
from seguridadApp.views import acceder

urlpatterns = [
    path('',include('seguridadApp.urls')), 
    path('admin/', admin.site.urls),
    path('categoria/', include('Categoria.urls')),
    path('clientes/', include('Clientes.urls')),
    path('productos/', include('Productos.urls')),
]
