from django.urls import path
from . import views

urlpatterns = [
    path('', views.categoria_list, name='categoria_list'),
]