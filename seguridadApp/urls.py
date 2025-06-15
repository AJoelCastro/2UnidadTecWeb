
from django.urls import path, include
from seguridadApp.views import acceder, homePage,salir
from django.contrib.auth import views as auth_views  # Si lo necesitas

urlpatterns = [
    path('', acceder, name="login"),
    path('home/', homePage, name="home"),
    path('logout/',salir,name="logout"),
]