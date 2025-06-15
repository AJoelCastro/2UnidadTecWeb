from django.contrib import admin
from django.urls import path,include
from seguridadApp.views import acceder

urlpatterns = [
    path('/', admin.site.urls),
]