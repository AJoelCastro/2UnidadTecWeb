from django.urls import path
from . import views

urlpatterns = [
    path('', views.producto_list, name='producto_list'),
]