from typing import Generic
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def acceder(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect("home")
                
    else:
        form = AuthenticationForm()
        
    return render(request, "login.html", {"form": form})

def homePage(request):
    return redirect(reverse('dashboard_ventas'))

def salir(request):
    messages.info(request, "Saliste exitosamente")
def logOut(request):
    logout(request)
    return redirect("login")